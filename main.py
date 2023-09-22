import cv2

image = cv2.imread("Haataja.jpg")
h, w, c = image.shape
scaler = 700 / h
#print(scaler)

new_height = h * scaler
new_width = w * scaler
dim = (int(new_width), int(new_height))
scaled_image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

# cropper for 2:3
# 700 / 3 * 2 = 466
a = new_width - 466
width_start = int(a / 2)
print(width_start)
width_end = width_start + 466
cropped_image = scaled_image[0:700, width_start:width_end]

# cropper for 3:4


# cropper for 9:16

#cv2.imshow("Image", image)
cv2.imshow("Cropped", cropped_image)
cv2.imshow("resized", scaled_image)
cv2.waitKey(0)
