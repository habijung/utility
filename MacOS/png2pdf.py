import os
import argparse
import cv2
import img2pdf


# Argument 관리
parser = argparse.ArgumentParser(description="PNG to PDF")
parser.add_argument("left", type=int, default=0, help="여백이 끝나는 x 좌표")
parser.add_argument("top", type=int, default=0, help="여백이 끝나는 y 좌표")
parser.add_argument(
    "-c", "--crop", default=False, action="store_true", help="단일 이미지 자르기 테스트"
)
parser.add_argument("-f", "--file", type=str, help="자르기 테스트에 사용할 파일명")
args = parser.parse_args()
print(args)


# Path 관리
dirname = os.path.dirname(__file__) + "/"
result = "result.pdf"


# 단일 파일 crop 테스트
if args.crop is True:
    print("단일 파일 crop 테스트")

    if args.file is None:
        print("Error: 추가된 파일이 없음")

    elif ".png" not in args.file:
        print("Error: PNG 파일이 아님")

    else:
        print("단일 파일 Crop 실행")
        print(f"파일명: {dirname + args.file}")

        image = cv2.imread(dirname + args.file)

        x, y = args.left, args.top
        h, w, c = image.shape
        image_crop = image[y : (h - y), x : (w - x)]

        cv2.imshow("Cropped Result", image_crop)
        cv2.waitKey(0)

# Convert PNG to PDF
else:
    print("png2pdf 실행")

    print("PNG 불러오는 중...")
    images = [file for file in sorted(os.listdir(dirname)) if ".png" in file]
    images_read = [cv2.imread(img) for img in images]

    print("PNG crop 작업 중...")
    x, y = args.left, args.top
    h, w, c = images_read[0].shape
    images_crop = [img[y : (h - y), x : (w - x)] for img in images_read]

    print("PNG crop 저장 중...")
    for i in range(len(images)):
        filename = "crop-" + images[i]
        img = images_crop[i]
        cv2.imwrite(dirname + filename, img)

    print("PNG crop 불러오는 중...")
    images_crop = [file for file in sorted(os.listdir(dirname)) if "crop-" in file]

    print("PNG -> PDF 변환 중...")
    with open(result, "wb") as f:
        f.write(img2pdf.convert(images_crop))

    for file in images_crop:
        os.remove(file)

    print("png2pdf 종료")
