%https://ch.mathworks.com/products/matlab/plot-gallery.html

%plot Sin(5x) and Exp(x) from x=0:2pi using 100 samples
%define the x values
x = linspace(0,pi,100);
y1 = sin(5*x);
y2 = exp(-x);

%plot the Sin with a red dotted line and x markers
figure
plot(x,y1,':rs')
hold on
plot(x,y2,':ko','MarkerFaceColor',[0.5,0.5,0.5])
% calculate the product of the two functions
prod=y1.*y2;

% Create a line plot and use the LineSpec option to specify a dashed green line with square markers. Use Name,Value pairs to specify the line width, marker size, and marker colors. Set the marker edge color to blue and set the marker face color using an RGB color value.
plot(x,prod,'-g','LineWidth',3)

%mark the point x(40),y1(40) with a black o marker and the following properties 'LineWidth',3, 'MarkerSize',15,'MarkerEdgeColor','k'

plot(x(40),y2(40),'-ko','LineWidth',3,'MarkerSize',15,'MarkerEdgeColor','k')

%disable the hold
hold off

%add annotations: title, axis descriptions and legends
title('2-D Line Plot')
xlabel('x-axis')
ylabel('y-axis')
legend('1st','2nd','3rd')

%set the x-axis limits to [0:2.5]
xlim([0 2.5])