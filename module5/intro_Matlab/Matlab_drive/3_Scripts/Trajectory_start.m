% -> change to live script -> mls extension

%Trajectory of a thrown object (format as title)

%Insert the picture Trajectory.jpg.

%In the absence of air, the trajectory of a thrown object is described by the following equations:
%replace the following code with formatted equations

x=v_0*cosd(a)*t;
y=v_0*sind(a)*t-0.5*9.81*t.^2;

%In this representaiton, x and y are the coordinates of the object, v0 the initial velocity, a the initial angle and t the time.

%add live control slider for a and v_0. Initialize them with the values
%given below
a = 50; 
v_0 =8;
t=0:0.01:5;

x=v_0*cosd(a)*t;
y=v_0*sind(a)*t-0.5*9.81*t.^2;

%Make a simple plot of the coordinates over time (x,y)

%limit the plot range of the axes to [0:10].
%add some meaningful legend and annotations.
