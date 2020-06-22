function viewDigitMontage(labelsTrain, imgDataTrain)
    warning off images:imshow:magnificationMustBeFitForDockedFigure
    perm = randperm(numel(labelsTrain), 25);
    subset = imgDataTrain(:,:,1,perm);
    montage(subset)
end