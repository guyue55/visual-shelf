// Preview an explicit independent seal without changing canonical rendering or templates.
// macOS / Swift, standard Apple frameworks only. Outputs are always unapproved drafts.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
import CryptoKit
func fail(_ message:String)->Never { fputs(message+"\n",stderr);exit(1) }
let args=Array(CommandLine.arguments.dropFirst())
if args.isEmpty || args.contains("--help") {
 print("swift scripts/preview_seal.swift --base logo.png --approved old.png --seal seal.png --x 0.825 --y 0.275 --width 0.065 --height 0.145 --color 463A33 --output .drafts/task/light\nCoordinates are CoreGraphics bottom-left fractions. Explicit preview only; no catalog or template updates.");exit(0)
}
var opts=[String:String]();var i=0
while i<args.count { guard args[i].hasPrefix("--"),i+1<args.count else { fail("参数须成对") };opts[String(args[i].dropFirst(2))]=args[i+1];i+=2 }
func value(_ key:String)->String { guard let v=opts[key] else { fail("缺少 --"+key) };return v }
func load(_ path:String)->CGImage { guard let src=CGImageSourceCreateWithURL(URL(fileURLWithPath:path) as CFURL,nil),let img=CGImageSourceCreateImageAtIndex(src,0,nil) else { fail("无法解码图像："+path) };return img }
func digest(_ path:String)->String { guard let data=try? Data(contentsOf:URL(fileURLWithPath:path)) else { fail("无法读取文件") };return SHA256.hash(data:data).map{String(format:"%02x",$0)}.joined() }
let root=URL(fileURLWithPath:#filePath).deletingLastPathComponent().deletingLastPathComponent().standardizedFileURL
let out=URL(fileURLWithPath:value("output")).standardizedFileURL
let fm=FileManager.default
let draftRoot=root.appendingPathComponent(".drafts").resolvingSymlinksInPath().path+"/"
guard out.resolvingSymlinksInPath().path.hasPrefix(draftRoot),!fm.fileExists(atPath:out.path) else { fail("只允许.drafts下的新目录，拒绝覆盖") }
let base=load(value("base")),old=load(value("approved")),seal=load(value("seal"))
guard base.width==old.width,base.height==old.height else { fail("基图与原图尺寸不一致") }
let cs=CGColorSpace(name:CGColorSpace.sRGB)!
func context(_ w:Int,_ h:Int)->CGContext { guard let c=CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:cs,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) else { fail("无法创建画布") };return c }
func write(_ im:CGImage,_ name:String) { guard let d=CGImageDestinationCreateWithURL(out.appendingPathComponent(name) as CFURL,UTType.png.identifier as CFString,1,nil) else { fail("无法输出PNG") };CGImageDestinationAddImage(d,im,nil);guard CGImageDestinationFinalize(d) else { fail("PNG保存失败") } }
let sc=context(seal.width,seal.height);sc.draw(seal,in:CGRect(x:0,y:0,width:seal.width,height:seal.height))
let sp=sc.data!.assumingMemoryBound(to:UInt8.self)
var minX=seal.width,minY=seal.height,maxX = -1,maxY = -1,transparent=0
for y in 0..<seal.height { for x in 0..<seal.width {let alpha=sp[(y*seal.width+x)*4+3];if alpha==0 { transparent+=1 };if alpha>0 {minX=min(minX,x);minY=min(minY,y);maxX=max(maxX,x);maxY=max(maxY,y)} } }
guard maxX>=0,transparent>0 else { fail("独立章须有非空笔迹及真正透明区域") }
let crop=CGRect(x:minX,y:minY,width:maxX-minX+1,height:maxY-minY+1)
guard let ink=seal.cropping(to:crop) else { fail("章裁切失败") }
let w=CGFloat(base.width),h=CGFloat(base.height)
func fraction(_ key:String)->CGFloat { guard let n=Double(value(key)),n.isFinite,n>=0,n<=1 else { fail("坐标必须为0..1有限数") };return CGFloat(n) }
let box=CGRect(x:fraction("x")*w,y:fraction("y")*h,width:fraction("width")*w,height:fraction("height")*h)
guard box.width>0,box.height>0,box.maxX<=w,box.maxY<=h else { fail("章框越界") }
let scale=min(box.width/CGFloat(ink.width),box.height/CGFloat(ink.height))
let rect=CGRect(x:box.midX-CGFloat(ink.width)*scale/2,y:box.midY-CGFloat(ink.height)*scale/2,width:CGFloat(ink.width)*scale,height:CGFloat(ink.height)*scale)
let hex=value("color");guard hex.count==6,let rgb=Int(hex,radix:16) else { fail("颜色为六位十六进制") }
let c=context(base.width,base.height);c.interpolationQuality = .high;c.draw(base,in:CGRect(x:0,y:0,width:w,height:h))
c.saveGState();c.clip(to:rect,mask:ink);c.setFillColor(CGColor(colorSpace:cs,components:[CGFloat((rgb>>16)&255)/255,CGFloat((rgb>>8)&255)/255,CGFloat(rgb&255)/255,1])!);c.fill(rect);c.restoreGState()
let final=c.makeImage()!
// Independently prove that the main image did not change outside the old/new seal region.
let oc=context(old.width,old.height);oc.draw(old,in:CGRect(x:0,y:0,width:w,height:h))
let a=c.data!.assumingMemoryBound(to:UInt8.self),b=oc.data!.assumingMemoryBound(to:UInt8.self)
let region=box.insetBy(dx:-3,dy:-3);var differentOutside=0
for py in 0..<base.height { for px in 0..<base.width { if region.contains(CGPoint(x:CGFloat(px)+0.5,y:h-CGFloat(py)-0.5)) { continue };let j=(py*base.width+px)*4;if (0..<4).contains(where:{a[j+$0] != b[j+$0]}) { differentOutside+=1 } } }
guard differentOutside==0 else { fail("章位区域之外与确认原图不一致：\(differentOutside)像素；拒绝误改正文或背景") }
try fm.createDirectory(at:out,withIntermediateDirectories:true)
write(final,"logo.png")
for size in [32,64,128,256] { let p=context(size,size);p.interpolationQuality = .high;p.draw(final,in:CGRect(x:0,y:0,width:size,height:size));write(p.makeImage()!,"preview-\(size).png") }
let record:[String:Any] = ["state":"awaiting-user","method":"fixed-source-alpha-mask; no glyph generation","seal_file":value("seal"),"seal_sha256":digest(value("seal")),"base_sha256":digest(value("base")),"approved_reference_sha256":digest(value("approved")),"png_sha256":digest(out.appendingPathComponent("logo.png").path),"color":hex,"seal_font":"unknown; source PNG outline","source_alpha_bounds":[minX,minY,maxX+1,maxY+1],"placement_box":[box.minX,box.minY,box.width,box.height],"actual_seal_bounds":[rect.minX,rect.minY,rect.width,rect.height],"aspect_preserved":true,"pixels_changed_outside_seal_region":differentOutside,"coordinate_system":"CoreGraphics bottom-left; PNG rows top-down","limitations":["original small raster seal; not an original vector font","not approved or archived; no platform acceptance"]]
try JSONSerialization.data(withJSONObject:record,options:[.prettyPrinted,.sortedKeys]).write(to:out.appendingPathComponent("preview.json"))
print("AWAITING USER: \(out.path)/logo.png; only seal region differs")
