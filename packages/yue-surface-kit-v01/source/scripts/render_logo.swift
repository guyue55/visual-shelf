import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data(("失败：" + message + "\n").utf8)); exit(1)
}
let argv = Array(CommandLine.arguments.dropFirst())
if argv.contains("--help") || argv.isEmpty {
    print("render-logo.sh --background FILE --font FILE --text 阅 --profile circle-logo|rounded-logo|square-master|cover|web|pwa-maskable|favicon|apple-touch|og-image|android-adaptive --theme light|dark --output DIR [--no-seal]")
    exit(0)
}
var options: [String:String] = [:]
var i = 0
while i < argv.count {
    if argv[i] == "--no-seal" { options["no-seal"] = "true"; i += 1; continue }
    guard argv[i].hasPrefix("--"), i + 1 < argv.count else { fail("参数必须成对") }
    options[String(argv[i].dropFirst(2))] = argv[i+1]; i += 2
}
let required = ["background", "font", "text", "profile", "theme", "output"]
for key in required { if options[key] == nil { fail("缺少 --" + key) } }
let text = options["text"]!
let characters = Array(text)
guard (1...12).contains(characters.count), !text.contains(where: { $0.isWhitespace }) else { fail("正文支持 1～12 个非空白字符，长标题请先明确断行方案") }
let profile = options["profile"]!
let allowed = ["circle-logo","rounded-logo","square-master","cover","web","pwa-maskable","favicon","apple-touch","og-image","android-adaptive"]
guard allowed.contains(profile), ["light","dark"].contains(options["theme"]!) else { fail("未知 profile 或 theme") }
if profile == "favicon" && characters.count > 2 { fail("标签图标最多两字；请先明确短标记，不能把长标题缩成字墙") }
let fm = FileManager.default
let output = URL(fileURLWithPath: options["output"]!, isDirectory:true)
guard !fm.fileExists(atPath:output.path) else { fail("输出目录已存在，拒绝覆盖") }
let fontURL = URL(fileURLWithPath:options["font"]!)
guard let data = CGDataProvider(url:fontURL as CFURL), let graphicsFont = CGFont(data) else { fail("字体文件无法加载") }
let font = CTFontCreateWithGraphicsFont(graphicsFont, 100, nil, nil)
let postScriptName = CTFontCopyPostScriptName(font) as String
func glyphPath(_ string: String) -> CGPath {
    var unicode = Array(string.utf16), glyphs = Array(repeating: CGGlyph(0), count:string.utf16.count)
    guard CTFontGetGlyphsForCharacters(font, &unicode, &glyphs, unicode.count), !glyphs.contains(0) else { fail("固定字体不包含字形：" + string + "；禁止静默换字体") }
    let path = CGMutablePath()
    for glyph in glyphs {
        guard let p = CTFontCreatePathForGlyph(font, glyph, nil) else { fail("无可用轮廓：" + string) }
        path.addPath(p)
    }
    return path
}
for char in characters { _ = glyphPath(String(char)) }
_ = glyphPath("古"); _ = glyphPath("月")
guard let imageSource = CGImageSourceCreateWithURL(URL(fileURLWithPath:options["background"]!) as CFURL,nil), let background = CGImageSourceCreateImageAtIndex(imageSource,0,nil) else { fail("背景无法解码") }
let width = profile == "cover" || profile == "web" ? 1600 : (profile == "og-image" ? 1200 : (profile == "apple-touch" ? 180 : (profile == "favicon" ? 256 : (profile == "android-adaptive" ? 1080 : 1024))))
let height = profile == "cover" ? 900 : (profile == "web" ? 600 : (profile == "og-image" ? 630 : width))
let w = CGFloat(width), h = CGFloat(height)
let colorSpace = CGColorSpace(name: CGColorSpace.sRGB)!
guard let context = CGContext(data:nil,width:width,height:height,bitsPerComponent:8,bytesPerRow:width*4,space:colorSpace,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) else { fail("无法创建画布") }
context.setAllowsAntialiasing(true); context.setShouldAntialias(true); context.interpolationQuality = .high
func color(_ hex: String) -> CGColor {
    let n = Int(hex,radix:16)!
    return CGColor(colorSpace:colorSpace,components:[CGFloat((n>>16)&255)/255,CGFloat((n>>8)&255)/255,CGFloat(n&255)/255,1])!
}
let dark = options["theme"] == "dark"
let ink = color(dark ? "F1E2BE" : "211F1B"), stampColor = color(dark ? "CF6650" : "A63A30")
var outline = CGPath(rect:CGRect(x:0,y:0,width:w,height:h),transform:nil)
if profile == "circle-logo" { outline = CGPath(ellipseIn:CGRect(x:w*0.025,y:h*0.025,width:w*0.95,height:h*0.95),transform:nil) }
if profile == "rounded-logo" { outline = CGPath(roundedRect:CGRect(x:w*0.045,y:h*0.045,width:w*0.91,height:h*0.91),cornerWidth:w*0.19,cornerHeight:h*0.19,transform:nil) }
context.addPath(outline); context.clip()
// Opaque fill under source alpha avoids transparent gaps inside the shape.
context.setFillColor(color(dark ? "102334" : "EAE2D2")); context.fill(CGRect(x:0,y:0,width:w,height:h))
let scale = max(w/CGFloat(background.width),h/CGFloat(background.height))
let bw = CGFloat(background.width)*scale, bh = CGFloat(background.height)*scale
if profile != "favicon" { context.draw(background,in:CGRect(x:(w-bw)/2,y:(h-bh)/2,width:bw,height:bh)) }
let backgroundLayer = context.makeImage()!
// Glyph paths, never synthesized lettering, fit uniformly into measured cells.
var glyphRecords: [[String:Any]] = []
var placedPaths: [CGPath] = []
func svgPath(_ path:CGPath) -> String {
    var parts:[String]=[]
    path.applyWithBlock { element in
        let e=element.pointee
        func point(_ i:Int)->String { "\(e.points[i].x) \(e.points[i].y)" }
        switch e.type {
        case .moveToPoint: parts.append("M"+point(0))
        case .addLineToPoint: parts.append("L"+point(0))
        case .addQuadCurveToPoint: parts.append("Q"+point(0)+" "+point(1))
        case .addCurveToPoint: parts.append("C"+point(0)+" "+point(1)+" "+point(2))
        case .closeSubpath: parts.append("Z")
        @unknown default: break
        }
    }
    return parts.joined(separator:" ")
}
func drawGlyph(_ value:String, _ cell:CGRect, _ fill:CGColor, _ role:String) {
    let p = glyphPath(value), b = p.boundingBoxOfPath
    let s = min(cell.width/b.width,cell.height/b.height)
    let x = cell.midX-b.width*s/2, y = cell.midY-b.height*s/2
    var matrix = CGAffineTransform(a:s,b:0,c:0,d:s,tx:x-b.minX*s,ty:y-b.minY*s)
    let placed = p.copy(using:&matrix)!
    context.setFillColor(fill); context.addPath(placed); context.fillPath()
    placedPaths.append(placed)
    let bounds = placed.boundingBoxOfPath
    glyphRecords.append(["text":value,"role":role,"x":bounds.minX,"y":bounds.minY,"width":bounds.width,"height":bounds.height,"svg_path":svgPath(placed)])
}
let landscape = width != height
let cols: Int
let rows: Int
if landscape { cols = min(characters.count,6); rows = (characters.count+cols-1)/cols }
else if characters.count == 1 { cols=1; rows=1 }
else if characters.count == 2 { cols=2; rows=1 }
else if characters.count <= 4 { cols=2; rows=2 }
else if characters.count <= 9 { cols=3; rows=(characters.count+2)/3 }
else { cols=4; rows=3 }
var box: CGRect
if landscape { box=CGRect(x:w*0.18,y:h*0.30,width:w*0.64,height:h*0.48) }
else if profile == "favicon" { box=CGRect(x:w*0.12,y:h*0.14,width:w*(options["no-seal"] == nil ? 0.62:0.76),height:h*0.72) }
else if profile == "android-adaptive" { box=CGRect(x:w*0.32,y:h*0.38,width:w*0.36,height:h*0.32) }
else if profile == "pwa-maskable" { box=CGRect(x:w*0.28,y:h*0.34,width:w*0.44,height:h*0.40) }
else if characters.count == 1 { box=CGRect(x:w*0.285,y:h*0.32,width:w*0.46,height:h*0.47) }
else { box=CGRect(x:w*0.25,y:h*0.34,width:w*0.49,height:h*0.44) }
for (index,char) in characters.enumerated() {
    let col=index%cols, row=index/cols
    let cellWidth=box.width/CGFloat(cols), cellHeight=box.height/CGFloat(rows)
    let rowCount=min(cols,characters.count-row*cols)
    let rowOffset=CGFloat(cols-rowCount)*cellWidth/2
    let cell=CGRect(x:box.minX+rowOffset+CGFloat(col)*cellWidth+cellWidth*0.04,y:box.maxY-CGFloat(row+1)*cellHeight+cellHeight*0.04,width:cellWidth*0.92,height:cellHeight*0.92)
    drawGlyph(String(char),cell,ink,"main")
}
let stamp: CGRect
if landscape { stamp=CGRect(x:w*0.84,y:h*0.31,width:h*0.09,height:h*0.19) }
else if profile == "favicon" { stamp=CGRect(x:w*0.79,y:h*0.25,width:w*0.10,height:h*0.25) }
else if profile == "android-adaptive" { stamp=CGRect(x:w*0.66,y:h*0.40,width:w*0.05,height:h*0.12) }
else if profile == "pwa-maskable" { stamp=CGRect(x:w*0.69,y:h*0.36,width:w*0.065,height:h*0.14) }
else { stamp=CGRect(x:w*0.77,y:h*0.35,width:w*0.075,height:h*0.17) }
if options["no-seal"] == nil {
    context.setStrokeColor(stampColor); context.setLineWidth(w*0.003)
    context.addPath(CGPath(roundedRect:stamp,cornerWidth:w*0.007,cornerHeight:w*0.007,transform:nil)); context.strokePath()
    let inset=stamp.insetBy(dx:stamp.width*0.12,dy:stamp.height*0.08)
    drawGlyph("古",CGRect(x:inset.minX,y:inset.midY,width:inset.width,height:inset.height*0.48),stampColor,"seal")
    drawGlyph("月",CGRect(x:inset.minX,y:inset.minY,width:inset.width,height:inset.height*0.48),stampColor,"seal")
}
guard let final = context.makeImage() else { fail("生成图像失败") }
try fm.createDirectory(at:output,withIntermediateDirectories:true)
func writePNG(_ image:CGImage,_ url:URL) {
    guard let destination=CGImageDestinationCreateWithURL(url as CFURL,UTType.png.identifier as CFString,1,nil) else { fail("无法输出 PNG") }
    CGImageDestinationAddImage(destination,image,nil)
    if !CGImageDestinationFinalize(destination) { fail("PNG 保存失败") }
}
writePNG(final,output.appendingPathComponent("logo.png"))
writePNG(backgroundLayer,output.appendingPathComponent("background-layer.png"))
let foregroundContext=CGContext(data:nil,width:width,height:height,bitsPerComponent:8,bytesPerRow:width*4,space:colorSpace,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
for (index,path) in placedPaths.enumerated() {
    foregroundContext.setFillColor((glyphRecords[index]["role"] as! String)=="main" ? ink:stampColor)
    foregroundContext.addPath(path); foregroundContext.fillPath()
}
if options["no-seal"] == nil {
    foregroundContext.setStrokeColor(stampColor);foregroundContext.setLineWidth(w*0.003)
    foregroundContext.addPath(CGPath(roundedRect:stamp,cornerWidth:w*0.007,cornerHeight:w*0.007,transform:nil));foregroundContext.strokePath()
}
writePNG(foregroundContext.makeImage()!,output.appendingPathComponent("foreground-layer.png"))
var svg="<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 \(width) \(height)\"><g transform=\"translate(0 \(height)) scale(1 -1)\">"
for rec in glyphRecords {
    let hex=(rec["role"] as! String)=="main" ? (dark ? "F1E2BE":"211F1B") : (dark ? "CF6650":"A63A30")
    svg += "<path d=\"\(rec["svg_path"] as! String)\" fill=\"#\(hex)\"/>"
}
if options["no-seal"] == nil {
    svg += "<rect x=\"\(stamp.minX)\" y=\"\(stamp.minY)\" width=\"\(stamp.width)\" height=\"\(stamp.height)\" rx=\"\(w*0.007)\" fill=\"none\" stroke=\"#\(dark ? "CF6650":"A63A30")\" stroke-width=\"\(w*0.003)\"/>"
}
svg += "</g></svg>"
try svg.write(to:output.appendingPathComponent("foreground.svg"),atomically:true,encoding:.utf8)
for size in [16,32,48,64,128,192,256,512] {
    let ph=Int(CGFloat(size)*h/w)
    let c=CGContext(data:nil,width:size,height:ph,bitsPerComponent:8,bytesPerRow:size*4,space:colorSpace,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
    c.interpolationQuality = .high; c.draw(final,in:CGRect(x:0,y:0,width:size,height:ph))
    writePNG(c.makeImage()!,output.appendingPathComponent("preview-\(size).png"))
}
var record: [String:Any] = ["profile":profile,"width":width,"height":height,"text":text,"font_postscript":postScriptName,"font_file":fontURL.path,"seal":options["no-seal"] == nil ? "古月" : "none","layout_columns":cols,"layout_rows":rows,"glyphs":glyphRecords,"color_space":"sRGB","background":options["background"]!,"theme":options["theme"]!,"state":"draft"]
record["os_version"] = ProcessInfo.processInfo.operatingSystemVersionString
record["all_glyph_bounds_inside_shape"] = glyphRecords.allSatisfy { rec in
    let x=rec["x"] as! CGFloat, y=rec["y"] as! CGFloat, gw=rec["width"] as! CGFloat, gh=rec["height"] as! CGFloat
    return [CGPoint(x:x,y:y),CGPoint(x:x+gw,y:y),CGPoint(x:x,y:y+gh),CGPoint(x:x+gw,y:y+gh)].allSatisfy { outline.contains($0) }
}
let pixels=context.data!.assumingMemoryBound(to:UInt8.self)
record["alpha_bottom_left"] = Int(pixels[3])
record["alpha_top_right"] = Int(pixels[(width*height-1)*4+3])
record["alpha_center"] = Int(pixels[((height/2)*width+width/2)*4+3])
if profile == "pwa-maskable" {
    let radius=w*0.4
    let valid=glyphRecords.allSatisfy { rec in
        let x=rec["x"] as! CGFloat, y=rec["y"] as! CGFloat, gw=rec["width"] as! CGFloat, gh=rec["height"] as! CGFloat
        return [CGPoint(x:x,y:y),CGPoint(x:x+gw,y:y),CGPoint(x:x,y:y+gh),CGPoint(x:x+gw,y:y+gh)].allSatisfy { point in hypot(point.x-w/2,point.y-h/2) <= radius }
    }
    record["maskable_glyph_safe_zone_passed"]=valid
    if !valid { fail("文字超出 PWA safe zone，不可交付") }
}
if profile == "android-adaptive" {
    let safe=glyphRecords.allSatisfy { rec in
        let x=rec["x"] as! CGFloat,y=rec["y"] as! CGFloat,gw=rec["width"] as! CGFloat,gh=rec["height"] as! CGFloat
        return [CGPoint(x:x,y:y),CGPoint(x:x+gw,y:y),CGPoint(x:x,y:y+gh),CGPoint(x:x+gw,y:y+gh)].allSatisfy { hypot($0.x-w/2,$0.y-h/2)<=w*33/108 }
    }
    record["android_glyph_safe_zone_passed"]=safe
    if !safe { fail("关键元素超出 Android 安全圆") }
}
let recordData=try JSONSerialization.data(withJSONObject:record,options:[.prettyPrinted,.sortedKeys])
try recordData.write(to:output.appendingPathComponent("render.json"))
print("DRAFT：\(output.path)/logo.png；字体 \(postScriptName)，\(cols)×\(rows) 字格，古月印章 \(options["no-seal"] == nil ? "on" : "off")")
