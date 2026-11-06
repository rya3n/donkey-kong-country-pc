/* Native GDI contract tests using synthetic pixels, no ROM or save files. */
#include "gdi_present.h"
#include "window_mode.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CHECK(x) do { if (!(x)) { fprintf(stderr, "line %d: %s\n", __LINE__, #x); exit(1); } } while (0)
typedef struct Target { HDC dc; HBITMAP bitmap; HGDIOBJ original; uint32_t *pixels; int w,h; } Target;

static Target MakeTarget(int w, int h) {
    Target t = {0};
    BITMAPINFO info = {0};
    info.bmiHeader.biSize = sizeof info.bmiHeader;
    info.bmiHeader.biWidth = w;
    info.bmiHeader.biHeight = -h;
    info.bmiHeader.biPlanes = 1;
    info.bmiHeader.biBitCount = 32;
    info.bmiHeader.biCompression = BI_RGB;
    t.dc = CreateCompatibleDC(NULL);
    t.bitmap = CreateDIBSection(t.dc, &info, DIB_RGB_COLORS, (void **)&t.pixels, NULL, 0);
    CHECK(t.dc && t.bitmap && t.pixels);
    t.original = SelectObject(t.dc, t.bitmap); CHECK(t.original && t.original != HGDI_ERROR);
    t.w = w; t.h = h;
    return t;
}
static void FreeTarget(Target *t) {
    SelectObject(t->dc, t->original); DeleteObject(t->bitmap); DeleteDC(t->dc);
}
static void Marker(Target *t) {
    CHECK(GdiFlush());
    for (int i=0;i<t->w*t->h;i++) t->pixels[i]=0x0013579bu;
}
static void Unchanged(const Target *t) {
    CHECK(GdiFlush());
    for (int i=0;i<t->w*t->h;i++) CHECK((t->pixels[i]&0xffffffu)==0x13579bu);
}
static void LegacyPaint(Target *t, const uint8_t *pixels) {
    RECT r = {0,0,t->w,t->h};
    FillRect(t->dc, &r, (HBRUSH)GetStockObject(BLACK_BRUSH));
    if (!pixels) {
        SetTextColor(t->dc,RGB(255,255,255));SetBkMode(t->dc,TRANSPARENT);
        DrawTextW(t->dc,L"Preparando o jogo...",-1,&r,DT_CENTER|DT_VCENTER|DT_SINGLELINE);
    } else {
        int w=t->w,h=w*3/4;
        if(h>t->h){h=t->h;w=h*4/3;}
        if(w>0&&h>0){
            BITMAPINFO b={0};b.bmiHeader.biSize=sizeof b.bmiHeader;
            b.bmiHeader.biWidth=256;b.bmiHeader.biHeight=-224;
            b.bmiHeader.biPlanes=1;b.bmiHeader.biBitCount=32;b.bmiHeader.biCompression=BI_RGB;
            SetStretchBltMode(t->dc,COLORONCOLOR);
            StretchDIBits(t->dc,(t->w-w)/2,(t->h-h)/2,w,h,0,0,256,224,pixels,&b,DIB_RGB_COLORS,SRCCOPY);
        }
    }
    CHECK(GdiFlush());
}

static BOOL CALLBACK CheckMonitor(HMONITOR monitor, HDC dc, LPRECT area, LPARAM unused) {
    (void)dc; (void)area; (void)unused;
    MONITORINFO info = {0}; info.cbSize = sizeof info;
    CHECK(GetMonitorInfoW(monitor, &info));
    HWND window = CreateWindowW(L"STATIC", L"DKC hidden window test", WS_OVERLAPPEDWINDOW,
        info.rcWork.left + 20, info.rcWork.top + 20, 320, 240, NULL, NULL, GetModuleHandleW(NULL), NULL);
    CHECK(window && !IsWindowVisible(window));
    LONG_PTR style = GetWindowLongPtrW(window, GWL_STYLE);
    WINDOWPLACEMENT before = {0}; before.length = sizeof before;
    CHECK(GetWindowPlacement(window, &before));
    Rev1WindowMode mode = {0};
    for (int repeat = 0; repeat < 20; repeat++) {
        CHECK(Rev1WindowFullscreen(window, &mode, 1));
        CHECK(mode.fullscreen && mode.monitor == monitor && !IsWindowVisible(window));
        RECT client; POINT origin = {0};
        CHECK(GetClientRect(window, &client) && ClientToScreen(window, &origin));
        CHECK(origin.x == info.rcMonitor.left && origin.y == info.rcMonitor.top);
        CHECK(client.right == info.rcMonitor.right - info.rcMonitor.left);
        CHECK(client.bottom == info.rcMonitor.bottom - info.rcMonitor.top);
        CHECK(Rev1WindowFullscreen(window, &mode, 1)); /* Refit, without replacing saved placement. */
        CHECK(Rev1WindowFullscreen(window, &mode, 0));
        CHECK(!mode.fullscreen && GetWindowLongPtrW(window, GWL_STYLE) == style);
        WINDOWPLACEMENT after = {0}; after.length = sizeof after;
        CHECK(GetWindowPlacement(window, &after));
        CHECK(EqualRect(&before.rcNormalPosition, &after.rcNormalPosition));
        CHECK(!IsWindowVisible(window));
    }
    CHECK(DestroyWindow(window));
    return TRUE;
}

int main(void) {
    uint32_t source[256*224];
    for(unsigned i=0;i<256*224;i++)source[i]=0xff000000u|((i*197u+1u)&0xffffffu);
    const int sizes[][2]={{768,576},{1000,600},{600,1000},{320,240},{1920,1080},{2560,1080},{1080,1920},{1,1}};
    Rev1GdiSurface surface={0};
    for(unsigned s=0;s<sizeof sizes/sizeof sizes[0];s++){
        Target actual=MakeTarget(sizes[s][0],sizes[s][1]);
        Target expected=MakeTarget(actual.w,actual.h);
        for(int loading=0;loading<2;loading++){
            const uint8_t *pixels=loading?NULL:(const uint8_t *)source;
            Marker(&actual);
            CHECK(Rev1GdiCompose(&surface,actual.dc,actual.w,actual.h,pixels,REV1_SCALE_4_3));
            Unchanged(&actual); /* No black intermediate frame on the destination. */
            CHECK(Rev1GdiPresent(&surface,actual.dc));
            LegacyPaint(&expected,pixels);
            for(int i=0;i<actual.w*actual.h;i++)
                CHECK((actual.pixels[i]&0xffffffu)==(expected.pixels[i]&0xffffffu));
        }
        Marker(&actual);
        CHECK(Rev1GdiCompose(&surface,actual.dc,actual.w,actual.h,(const uint8_t *)source,REV1_SCALE_FILL));
        Unchanged(&actual);
        CHECK(Rev1GdiPresent(&surface,actual.dc));
        BITMAPINFO b = {0}; b.bmiHeader.biSize=sizeof b.bmiHeader;
        b.bmiHeader.biWidth=256;b.bmiHeader.biHeight=-224;
        b.bmiHeader.biPlanes=1;b.bmiHeader.biBitCount=32;b.bmiHeader.biCompression=BI_RGB;
        SetStretchBltMode(expected.dc,COLORONCOLOR);
        CHECK(StretchDIBits(expected.dc,0,0,actual.w,actual.h,0,0,256,224,source,&b,DIB_RGB_COLORS,SRCCOPY));
        CHECK(GdiFlush());
        for(int i=0;i<actual.w*actual.h;i++) {
            CHECK((actual.pixels[i]&0xffffffu)==(expected.pixels[i]&0xffffffu));
            CHECK(actual.pixels[i]&0xffffffu); /* Nonblack source must cover every destination pixel. */
        }
        HBITMAP previous=surface.bitmap;
        CHECK(!Rev1GdiCompose(&surface,actual.dc,0,actual.h,(const uint8_t *)source,REV1_SCALE_FILL));
        CHECK(surface.bitmap==previous && surface.complete);
        FreeTarget(&actual);FreeTarget(&expected);
    }
    Rev1GdiFree(&surface);
    Target target=MakeTarget(320,240);
    memset(source,0,sizeof source);
    CHECK(Rev1GdiCompose(&surface,target.dc,320,240,(const uint8_t *)source,REV1_SCALE_FILL));
    CHECK(Rev1GdiPresent(&surface,target.dc));
    for(int i=0;i<320*240;i++)CHECK(!(target.pixels[i]&0xffffffu)); /* Real guest fades remain black. */
    Rev1GdiFree(&surface);
    DWORD before=GetGuiResources(GetCurrentProcess(),GR_GDIOBJECTS);
    for(int i=0;i<500;i++){
        CHECK(Rev1GdiCompose(&surface,target.dc,320+(i&1),240,(const uint8_t *)source,
                             i&1 ? REV1_SCALE_FILL : REV1_SCALE_4_3));
        CHECK(Rev1GdiPresent(&surface,target.dc));
    }
    Rev1GdiFree(&surface);
    CHECK(GetGuiResources(GetCurrentProcess(),GR_GDIOBJECTS)==before);
    FreeTarget(&target);
    CHECK(EnumDisplayMonitors(NULL,NULL,CheckMonitor,0));
    puts("GDI: fill covers eight sizes, original 4:3 matches, offscreen isolation/black/loading/resources passed");
    puts("Window: hidden fullscreen/refit/restoration passed on all connected monitors (20 cycles each)");
    return 0;
}
