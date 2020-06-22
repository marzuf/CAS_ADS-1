function iFinal = preprocessImage(iOriginal)
% Function to resize and preprocess each image
% 
% Copyright 2017 The MathWorks, Inc.

dim = size(iOriginal);

iGray = rgb2gray(iOriginal);

%Match input image with color pattern of training set
BW_Threshold = graythresh(iGray)/2;
iBW = imcomplement(imbinarize(iGray,BW_Threshold));

%Prepare variables for while loop
h = dim(1);
w = dim(2);
iDilated = iBW;

while h > 28 && w > 28
    
    %Iterate between shrinking and dilating image
    iShrink = imresize(iDilated,[h w]);
    
    strelSize = floor(mean([h w]/115));
    SE = strel('diamond', strelSize);
    iDilated = imdilate(iShrink, SE);
    
    h = floor(h/2);
    w = floor(w/2);
end

iFinal = im2uint8(imresize(iDilated, [28 28]));

end