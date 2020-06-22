function f=mathfunction(x)
%some help or description line
f=zeros(length(x),1);
for n=1:length(x)
    if x(n) < -3*pi
        f(n)=-1;
    elseif x(n)>4*pi
        f(n)=1;
    else
        f(n)=cos(x(n));
    end
end
end