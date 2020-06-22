function [top3,sortedV]=getLargest3(v)
% GETLARGEST3 returns the 3 largest elements of the input v
% getLargest3(v) sorts v in descending order and returns the elements 1:3

sortedV=sort(v,'descend');
if length(v)>3
    top3=sortedV(1:3);
else
    top3=sortedV;
end