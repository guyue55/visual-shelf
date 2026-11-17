// Specific source-B extraction recipe; output remains an unapproved raster mask.
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers
import CryptoKit
func fail(_ message:String)->Never { fputs(message+"\n",stderr);exit(1) }
let args=CommandLine.arguments
if args.count != 3 || args.contains("--help") { print("swift scripts/extract_seal_b.swift SOURCE.png .drafts/task/seal.png — fixed, unapproved original-B ink mask");exit(args.contains("--help") ? 0:1) }
let root=URL(fileURLWithPath:#filePath).deletingLastPathComponent().deletingLastPathComponent()
let output=URL(fileURLWithPath:args[2]).standardizedFileURL
let allowed=root.appendingPathComponent(".drafts").resolvingSymlinksInPath().path+"/"
guard output.resolvingSymlinksInPath().path.hasPrefix(allowed),!FileManager.default.fileExists(atPath:output.path) else { fail("only a new .drafts output is allowed") }
let sourceData=try Data(contentsOf:URL(fileURLWithPath:args[1]))
let hash=SHA256.hash(data:sourceData).map{String(format:"%02x",$0)}.joined()
guard hash=="b2c0a629af3dbad2dff081514f84c14207d7191d704f2ff8e663fca238497604" else { fail("source is not the verified light-B reference") }
try FileManager.default.createDirectory(at:output.deletingLastPathComponent(),withIntermediateDirectories:true)
let src=CGImageSourceCreateWithURL(URL(fileURLWithPath:args[1]) as CFURL,nil)!
let im=CGImageSourceCreateImageAtIndex(src,0,nil)!
let cs=CGColorSpace(name:CGColorSpace.sRGB)!
let w=im.width,h=im.height
let ctx=CGContext(data:nil,width:w,height:h,bitsPerComponent:8,bytesPerRow:w*4,space:cs,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(im,in:CGRect(x:0,y:0,width:w,height:h))
let bytes=ctx.data!.assumingMemoryBound(to:UInt8.self)
let x0=776,y0=721,cw=64,ch=114
let out=CGContext(data:nil,width:cw,height:ch,bitsPerComponent:8,bytesPerRow:cw*4,space:cs,bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue)!
let b=out.data!.assumingMemoryBound(to:UInt8.self)
for y in 0..<ch { for x in 0..<cw {
 let i=((y+y0)*w+x+x0)*4,j=(y*cw+x)*4
 let lum=(Double(bytes[i])+Double(bytes[i+1])+Double(bytes[i+2]))/3
 let alpha=max(0,min(1,(145-lum)/55))
 b[j]=UInt8(70*alpha);b[j+1]=UInt8(58*alpha);b[j+2]=UInt8(51*alpha);b[j+3]=UInt8(255*alpha)
}}
let dest=CGImageDestinationCreateWithURL(URL(fileURLWithPath:args[2]) as CFURL,UTType.png.identifier as CFString,1,nil)!
CGImageDestinationAddImage(dest,out.makeImage()!,nil);CGImageDestinationFinalize(dest)
