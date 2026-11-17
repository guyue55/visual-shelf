// Export the two approved theme colors, preserving every source alpha pixel.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
import CryptoKit
func fail(_ message:String)->Never { fputs(message+"\n",stderr);exit(1) }
let args=Array(CommandLine.arguments.dropFirst())
if args.count != 1 || args.contains("--help") { print("swift scripts/export_seal_colors.swift .drafts/NEW-TASK\nExports the approved A63A30 / CF6650 variants, never overwrites.");exit(args.contains("--help") ? 0:1) }
let root=URL(fileURLWithPath:#filePath).deletingLastPathComponent().deletingLastPathComponent()
let fm=FileManager.default,out=URL(fileURLWithPath:args[0]).standardizedFileURL
let allowed=root.appendingPathComponent(".drafts").resolvingSymlinksInPath().path+"/"
guard out.resolvingSymlinksInPath().path.hasPrefix(allowed),!fm.fileExists(atPath:out.path) else { fail("输出须为.drafts下新目录") }
let config=try JSONSerialization.jsonObject(with:Data(contentsOf:root.appendingPathComponent("resources/seals/guyue-b/provenance.json"))) as! [String:Any]
let source=root.appendingPathComponent(config["path"] as! String)
func sha(_ url:URL)->String { SHA256.hash(data:try! Data(contentsOf:url)).map{String(format:"%02x",$0)}.joined() }
guard sha(source)==config["sha256"] as? String else { fail("章源SHA漂移") }
let cs=CGColorSpace(name:CGColorSpace.sRGB)!
func load(_ url:URL)->CGImage { guard let s=CGImageSourceCreateWithURL(url as CFURL,nil),let im=CGImageSourceCreateImageAtIndex(s,0,nil) else { fail("无法解码PNG") };return im }
func pixels(_ im:CGImage)->CGContext { let c=CGContext(data:nil,width:im.width,height:im.height,bitsPerComponent:8,bytesPerRow:im.width*4,space:cs,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!;c.draw(im,in:CGRect(x:0,y:0,width:im.width,height:im.height));return c }
let im=load(source),src=pixels(im),a=src.data!.assumingMemoryBound(to:UInt8.self)
guard im.width==64,im.height==114 else { fail("章源尺寸漂移") }
try fm.createDirectory(at:out,withIntermediateDirectories:true)
var variants=[[String:Any]]()
for (theme,hex) in [("light","A63A30"),("dark","CF6650")] {
 let rgb=Int(hex,radix:16)!,channels=[(rgb>>16)&255,(rgb>>8)&255,rgb&255]
 let c=pixels(im),b=c.data!.assumingMemoryBound(to:UInt8.self)
 for i in stride(from:0,to:im.width*im.height*4,by:4) { let alpha=Int(a[i+3]);for k in 0..<3 {b[i+k]=UInt8((channels[k]*alpha+127)/255)};b[i+3]=a[i+3] }
 let file=out.appendingPathComponent("seal-"+theme+".png")
 let d=CGImageDestinationCreateWithURL(file as CFURL,UTType.png.identifier as CFString,1,nil)!
 CGImageDestinationAddImage(d,c.makeImage()!,nil);guard CGImageDestinationFinalize(d) else { fail("PNG写入失败") }
 // Decode the actual saved PNG for an independent alpha/color comparison.
 let decoded=pixels(load(file)),p=decoded.data!.assumingMemoryBound(to:UInt8.self)
 var opaque=0
 for i in stride(from:0,to:im.width*im.height*4,by:4) {
  guard p[i+3]==a[i+3] else { fail("透明度改变") }
  if p[i+3]==255 {opaque+=1;guard (0..<3).allSatisfy({Int(p[i+$0])==channels[$0]}) else { fail("实际PNG核心颜色不符") }}
 }
 guard opaque>0 else { fail("缺少可核对的实色像素") }
 variants.append(["theme":theme,"color":hex,"file":file.lastPathComponent,"sha256":sha(file),"dimensions":[64,114],"all_alpha_pixels_equal":true,"opaque_rgb_exact":true,"source_sha256":sha(source)])
}
try JSONSerialization.data(withJSONObject:["source_asset":config["id"]!,"variants":variants],options:[.prettyPrinted,.sortedKeys]).write(to:out.appendingPathComponent("colors.json"))
print("固定章两色导出并复核通过：\(out.path)")
