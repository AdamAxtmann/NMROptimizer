#param size := 11;
#param max_rad := 1000;
param pi := acos(-1);
#param max_angl := 17;
#param max_odm := 35;
#adding an array of arbitrary angles

# param odm_per_cm := 4;
# param dose_per_cm := 4;

param odm_radius_cm := 35;
param odm_per_cm := 4;
param dose_per_cm := 4;
param max_odm := odm_per_cm * odm_radius_cm*2;# to avoid error
param source_distance_cm := 100;
param n := 7;
set ANGLES := {10, 50, 90, 130, 170, 200, 340};


var rad{angle in ANGLES, offset in {-max_odm..max_odm}} >= 0;

#param max_at_risk := 6;
#param min_at_tumor := 10;

param t{i in {-53..53},j in {-75..75}, angle in ANGLES} = (i/dose_per_cm*cos(angle*pi/180)+j/dose_per_cm*sin(angle*pi/180))/(i/dose_per_cm*cos(angle*pi/180)+j/dose_per_cm*sin(angle*pi/180)-source_distance_cm);
param s {i in{-53..53}, j in {-75..75}, angle in ANGLES} :=  odm_per_cm * (-sin(angle*pi/180)*(i/dose_per_cm+t[i,j,angle]*(source_distance_cm*cos(angle*pi/180)-i/dose_per_cm)) +  cos(angle*pi/180)*(j/dose_per_cm+t[i,j,angle]*(source_distance_cm*sin(angle*pi/180)-j/dose_per_cm)));

param s_int {i in{-53..53}, j in {-75..75}, angle in ANGLES} := floor(s[i,j,angle]);
param s_frac {i in{-53..53}, j in {-75..75}, angle in ANGLES} := s[i,j,angle]- s_int[i,j,angle]; 
param s_frac1 {i in{-53..53}, j in {-75..75}, angle in ANGLES} := 1 - s_frac[i,j,angle];
var dose {i in {-53..53}, j in {-75..75}};

param geom {i in {-53..53}, j in {-75..75}, angle in ANGLES} := source_distance_cm*source_distance_cm/ (((source_distance_cm*cos(angle*pi/180)- i/dose_per_cm)^2)+
(source_distance_cm*sin(angle*pi/180)-j/dose_per_cm)^2);

var t2{angle in ANGLES, offset in {-max_odm+1..max_odm}} >= 0;

subject to constT12 {angle in ANGLES, offset in{-max_odm+1..max_odm}}:
        t2[angle,offset] >= rad[angle,offset] - rad[angle,offset-1];
subject to constT21 {angle in ANGLES, offset in {-max_odm+1..max_odm}}:
        -t2[angle,offset] <= rad[angle,offset] - rad[angle,offset-1];
#--------------------------------------------------------


#--------------------------------------------------------

subject to test{i in {ANGLES}, j in{-max_odm..max_odm}}: rad[i,j] <= 36;


subject to const3 {i in {-53..53}, j in {-75..75}}:
	dose[i,j] =sum {angle in ANGLES}geom[i,j,angle]*((s_frac1[i,j,angle])*rad[angle,s_int[i,j,angle]]+(s_frac[i,j,angle])*rad[angle,1+s_int[i, j, angle]]);

 #param max_tumor;

#---------------------------------------------------------------------------------
subject to const_68 {(i,j) in {(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),(-2,4),
	(-1,-8),(-1,-7),(-1,-6),(-1,-5),(-1,-4),(-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),(-1,4),
	(-1,5),(0,-10),(0,-9),(0,-8),(0,-7),(0,-6),(0,-5),(0,-4),(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),
	(0,3),(0,4),(0,5),(0,6),(1,-11),(1,-10),(1,-9),(1,-8),(1,-7),(1,-6),(1,-5),(1,-4),(1,-3),(1,-2),
	(1,-1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,-12),(2,-11),(2,-10),(2,-9),(2,-8),(2,-7),
	(2,-6),(2,-5),(2,-4),(2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),
	(3,-13),(3,-12),(3,-11),(3,-10),(3,-9),(3,-8),(3,-7),(3,-6),(3,-5),(3,-4),(3,-3),(3,-2),(3,-1),
	(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(4,-14),(4,-13),(4,-12),(4,-11),
	(4,-10),(4,-9),(4,-8),(4,-7),(4,-6),(4,-5),(4,-4),(4,-3),(4,-2),(4,-1),(4,0),(4,1),(4,2),(4,3),
	(4,4),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),(5,-14),(5,-13),(5,-12),(5,-11),(5,-10),(5,-9),(5,-8),
	(5,-7),(5,-6),(5,-5),(5,-4),(5,-3),(5,-2),(5,-1),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),
	(5,8),(5,9),(5,10),(6,-15),(6,-14),(6,-13),(6,-12),(6,-11),(6,-10),(6,-9),(6,-8),(6,-7),(6,-6),
	(6,-5),(6,-4),(6,-3),(6,-2),(6,-1),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),
	(6,10),(7,-15),(7,-14),(7,-13),(7,-12),(7,-11),(7,-10),(7,-9),(7,-8),(7,-7),(7,-6),(7,-5),(7,-4),
	(7,-3),(7,-2),(7,-1),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11),
	(8,-15),(8,-14),(8,-13),(8,-12),(8,-11),(8,-10),(8,-9),(8,-8),(8,-7),(8,-6),(8,-5),(8,-4),(8,-3),
	(8,-2),(8,-1),(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10),(8,11),(8,12),
	(9,-15),(9,-14),(9,-13),(9,-12),(9,-11),(9,-10),(9,-9),(9,-8),(9,-7),(9,-6),(9,-5),(9,-4),(9,-3),
	(9,-2),(9,-1),(9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),(9,11),(9,12),
	(10,-15),(10,-14),(10,-13),(10,-12),(10,-11),(10,-10),(10,-9),(10,-8),(10,-7),(10,-6),(10,-5),
	(10,-4),(10,-3),(10,-2),(10,-1),(10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),
	(10,9),(10,10),(10,11),(10,12),(11,-15),(11,-14),(11,-13),(11,-12),(11,-11),(11,-10),(11,-9),
	(11,-8),(11,-7),(11,-6),(11,-5),(11,-4),(11,-3),(11,-2),(11,-1),(11,0),(11,1),(11,2),(11,3),
	(11,4),(11,5),(11,6),(11,7),(11,8),(11,9),(11,10),(11,11),(11,12),(12,-15),(12,-14),(12,-13),
	(12,-12),(12,-11),(12,-10),(12,-9),(12,-8),(12,-7),(12,-6),(12,-5),(12,-4),(12,-3),(12,-2),
	(12,-1),(12,0),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),
	(12,12),(13,-15),(13,-14),(13,-13),(13,-12),(13,-11),(13,-10),(13,-9),(13,-8),(13,-7),(13,-6),
	(13,-5),(13,-4),(13,-3),(13,-2),(13,-1),(13,0),(13,1),(13,2),(13,3),(13,4),(13,5),(13,6),(13,7),
	(13,8),(13,9),(13,10),(13,11),(13,12),(14,-15),(14,-14),(14,-13),(14,-12),(14,-11),(14,-10),
	(14,-9),(14,-8),(14,-7),(14,-6),(14,-5),(14,-4),(14,-3),(14,-2),(14,-1),(14,0),(14,1),(14,2),
	(14,3),(14,4),(14,5),(14,6),(14,7),(14,8),(14,9),(14,10),(14,11),(14,12),(15,-15),(15,-14),
	(15,-13),(15,-12),(15,-11),(15,-10),(15,-9),(15,-8),(15,-7),(15,-6),(15,-5),(15,-4),(15,-3),
	(15,-2),(15,-1),(15,0),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),(15,8),(15,9),(15,10),
	(15,11),(15,12),(16,-15),(16,-14),(16,-13),(16,-12),(16,-11),(16,-10),(16,-9),(16,-8),(16,-7),
	(16,-6),(16,-5),(16,-4),(16,-3),(16,-2),(16,-1),(16,0),(16,1),(16,2),(16,3),(16,4),(16,5),
	(16,6),(16,7),(16,8),(16,9),(16,10),(16,11),(16,12),(17,-15),(17,-14),(17,-13),(17,-12),
	(17,-11),(17,-10),(17,-9),(17,-8),(17,-7),(17,-6),(17,-5),(17,-4),(17,-3),(17,-2),(17,-1),
	(17,0),(17,1),(17,2),(17,3),(17,4),(17,5),(17,6),(17,7),(17,8),(17,9),(17,10),(17,11),(18,-14),
	(18,-13),(18,-12),(18,-11),(18,-10),(18,-9),(18,-8),(18,-7),(18,-6),(18,-5),(18,-4),(18,-3),
	(18,-2),(18,-1),(18,0),(18,1),(18,2),(18,3),(18,4),(18,5),(18,6),(18,7),(18,8),(18,9),(18,10),
(18,11)}}: dose[i,j] >= 95;

subject to const1_68 {(i,j) in {(-2,-4),(-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),
	(-2,4),(-1,-8),(-1,-7),(-1,-6),(-1,-5),(-1,-4),(-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),
	(-1,3),(-1,4),(-1,5),(0,-10),(0,-9),(0,-8),(0,-7),(0,-6),(0,-5),(0,-4),(0,-3),(0,-2),(0,-1),
	(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,-11),(1,-10),(1,-9),(1,-8),(1,-7),(1,-6),(1,-5),
	(1,-4),(1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,-12),(2,-11),
	(2,-10),(2,-9),(2,-8),(2,-7),(2,-6),(2,-5),(2,-4),(2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),
	(2,4),(2,5),(2,6),(2,7),(2,8),(3,-13),(3,-12),(3,-11),(3,-10),(3,-9),(3,-8),(3,-7),(3,-6),(3,-5),
	(3,-4),(3,-3),(3,-2),(3,-1),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(4,-14),
	(4,-13),(4,-12),(4,-11),(4,-10),(4,-9),(4,-8),(4,-7),(4,-6),(4,-5),(4,-4),(4,-3),(4,-2),(4,-1),
	(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),(4,9),(4,10),(5,-14),(5,-13),(5,-12),(5,-11),
	(5,-10),(5,-9),(5,-8),(5,-7),(5,-6),(5,-5),(5,-4),(5,-3),(5,-2),(5,-1),(5,0),(5,1),(5,2),(5,3),(5,4)
	,(5,5),(5,6),(5,7),(5,8),(5,9),(5,10),(6,-15),(6,-14),(6,-13),(6,-12),(6,-11),(6,-10),(6,-9),(6,-8),(6,-7),
	(6,-6),(6,-5),(6,-4),(6,-3),(6,-2),(6,-1),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),
	(6,10),(7,-15),(7,-14),(7,-13),(7,-12),(7,-11),(7,-10),(7,-9),(7,-8),(7,-7),(7,-6),(7,-5),(7,-4),(7,-3),
	(7,-2),(7,-1),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(7,11),(8,-15),(8,-14),
	(8,-13),(8,-12),(8,-11),(8,-10),(8,-9),(8,-8),(8,-7),(8,-6),(8,-5),(8,-4),(8,-3),(8,-2),(8,-1),(8,0),
	(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,10),(8,11),(8,12),(9,-15),(9,-14),(9,-13),
	(9,-12),(9,-11),(9,-10),(9,-9),(9,-8),(9,-7),(9,-6),(9,-5),(9,-4),(9,-3),(9,-2),(9,-1),(9,0),(9,1),
	(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,10),(9,11),(9,12),(10,-15),(10,-14),(10,-13),(10,-12),
	(10,-11),(10,-10),(10,-9),(10,-8),(10,-7),(10,-6),(10,-5),(10,-4),(10,-3),(10,-2),(10,-1),(10,0),(10,1),
	(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12),(11,-15),(11,-14),(11,-13),
	(11,-12),(11,-11),(11,-10),(11,-9),(11,-8),(11,-7),(11,-6),(11,-5),(11,-4),(11,-3),(11,-2),(11,-1),(11,0),
	(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(11,7),(11,8),(11,9),(11,10),(11,11),(11,12),(12,-15),(12,-14),
	(12,-13),(12,-12),(12,-11),(12,-10),(12,-9),(12,-8),(12,-7),(12,-6),(12,-5),(12,-4),(12,-3),(12,-2),(12,-1),
	(12,0),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12,12),(13,-15),
	(13,-14),(13,-13),(13,-12),(13,-11),(13,-10),(13,-9),(13,-8),(13,-7),(13,-6),(13,-5),(13,-4),(13,-3),
	(13,-2),(13,-1),(13,0),(13,1),(13,2),(13,3),(13,4),(13,5),(13,6),(13,7),(13,8),(13,9),(13,10),(13,11),
	(13,12),(14,-15),(14,-14),(14,-13),(14,-12),(14,-11),(14,-10),(14,-9),(14,-8),(14,-7),(14,-6),(14,-5),
	(14,-4),(14,-3),(14,-2),(14,-1),(14,0),(14,1),(14,2),(14,3),(14,4),(14,5),(14,6),(14,7),(14,8),(14,9),
	(14,10),(14,11),(14,12),(15,-15),(15,-14),(15,-13),(15,-12),(15,-11),(15,-10),(15,-9),(15,-8),(15,-7),
	(15,-6),(15,-5),(15,-4),(15,-3),(15,-2),(15,-1),(15,0),(15,1),(15,2),(15,3),(15,4),(15,5),(15,6),(15,7),
	(15,8),(15,9),(15,10),(15,11),(15,12),(16,-15),(16,-14),(16,-13),(16,-12),(16,-11),(16,-10),(16,-9),
	(16,-8),(16,-7),(16,-6),(16,-5),(16,-4),(16,-3),(16,-2),(16,-1),(16,0),(16,1),(16,2),(16,3),(16,4),
	(16,5),(16,6),(16,7),(16,8),(16,9),(16,10),(16,11),(16,12),(17,-15),(17,-14),(17,-13),(17,-12),(17,-11),
	(17,-10),(17,-9),(17,-8),(17,-7),(17,-6),(17,-5),(17,-4),(17,-3),(17,-2),(17,-1),(17,0),(17,1),(17,2),
	(17,3),(17,4),(17,5),(17,6),(17,7),(17,8),(17,9),(17,10),(17,11),(18,-14),(18,-13),(18,-12),(18,-11),
	(18,-10),(18,-9),(18,-8),(18,-7),(18,-6),(18,-5),(18,-4),(18,-3),(18,-2),(18,-1),(18,0),(18,1),(18,2),
	(18,3),(18,4),(18,5),(18,6),(18,7),(18,8),(18,9),(18,10),
(18,11)}}: dose[i,j] <= 105;

#-----------------------------------------------------------------------------------
param max_s := 25;

subject to const_2:(sum {(i,j) in {(-25,-2),(-25,-1),(-24,-9),(-24,-8),(-24,-7),(-24,-6),(-24,-5),(-24,-4),
	(-24,-3),(-24,-2),(-24,-1),(-24,0),(-24,1),(-24,2),(-24,3),(-24,4),(-23,-10),(-23,-9),(-23,-8),(-23,-7),
	(-23,-6),(-23,-5),(-23,-4),(-23,-3),(-23,-2),(-23,-1),(-23,0),(-23,1),(-23,2),(-23,3),(-23,4),(-23,5),
	(-23,6),(-22,-11),(-22,-10),(-22,-9),(-22,-8),(-22,-7),(-22,-6),(-22,-5),(-22,-4),(-22,-3),(-22,-2),
	(-22,-1),(-22,0),(-22,1),(-22,2),(-22,3),(-22,4),(-22,5),(-22,6),(-22,7),(-22,8),(-21,-12),(-21,-11),
	(-21,-10),(-21,-9),(-21,-8),(-21,-7),(-21,-6),(-21,-5),(-21,-4),(-21,-3),(-21,-2),(-21,-1),(-21,0),
	(-21,1),(-21,2),(-21,3),(-21,4),(-21,5),(-21,6),(-21,7),(-21,8),(-21,9),(-21,10),(-20,-13),(-20,-12),
	(-20,-11),(-20,-10),(-20,-9),(-20,-8),(-20,-7),(-20,-6),(-20,-5),(-20,-4),(-20,-3),(-20,-2),(-20,-1),
	(-20,0),(-20,1),(-20,2),(-20,3),(-20,4),(-20,5),(-20,6),(-20,7),(-20,8),(-20,9),(-20,10),(-19,-13),
	(-19,-12),(-19,-11),(-19,-10),(-19,-9),(-19,-8),(-19,-7),(-19,-6),(-19,-5),(-19,-4),(-19,-3),(-19,-2),
	(-19,-1),(-19,0),(-19,1),(-19,2),(-19,3),(-19,4),(-19,5),(-19,6),(-19,7),(-19,8),(-19,9),(-19,10),
	(-19,11),(-18,-13),(-18,-12),(-18,-11),(-18,-10),(-18,-9),(-18,-8),(-18,-7),(-18,-6),(-18,-5),(-18,-4),
	(-18,-3),(-18,-2),(-18,-1),(-18,0),(-18,1),(-18,2),(-18,3),(-18,4),(-18,5),(-18,6),(-18,7),(-18,8),
	(-18,9),(-18,10),(-18,11),(-17,-13),(-17,-12),(-17,-11),(-17,-10),(-17,-9),(-17,-8),(-17,-7),(-17,-6),
	(-17,-5),(-17,-4),(-17,-3),(-17,-2),(-17,-1),(-17,0),(-17,1),(-17,2),(-17,3),(-17,4),(-17,5),(-17,6),
	(-17,7),(-17,8),(-17,9),(-17,10),(-17,11),(-16,-13),(-16,-12),(-16,-11),(-16,-10),(-16,-9),(-16,-8),
	(-16,-7),(-16,-6),(-16,-5),(-16,-4),(-16,-3),(-16,-2),(-16,-1),(-16,0),(-16,1),(-16,2),(-16,3),(-16,4),
	(-16,5),(-16,6),(-16,7),(-16,8),(-16,9),(-16,10),(-16,11),(-15,-13),(-15,-12),(-15,-11),(-15,-10),
	(-15,-9),(-15,-8),(-15,-7),(-15,-6),(-15,-5),(-15,-4),(-15,-3),(-15,-2),(-15,-1),(-15,0),(-15,1),(-15,2),
	(-15,3),(-15,4),(-15,5),(-15,6),(-15,7),(-15,8),(-15,9),(-15,10),(-14,-12),(-14,-11),(-14,-10),(-14,-9),
	(-14,-8),(-14,-7),(-14,-6),(-14,-5),(-14,-4),(-14,-3),(-14,-2),(-14,-1),(-14,0),(-14,1),(-14,2),(-14,3),
	(-14,4),(-14,5),(-14,6),(-14,7),(-14,8),(-14,9),(-14,10),(-13,-12),(-13,-11),(-13,-10),(-13,-9),(-13,-8),
	(-13,-7),(-13,-6),(-13,-5),(-13,-4),(-13,-3),(-13,-2),(-13,-1),(-13,0),(-13,1),(-13,2),(-13,3),(-13,4),
	(-13,5),(-13,6),(-13,7),(-13,8),(-13,9),(-13,10),(-12,-12),(-12,-11),
	(-12,-10),(-12,-9),(-12,-8),(-12,-7),(-12,-6),(-12,-5),(-12,-4),(-12,-3),(-12,-2),(-12,-1),(-12,0),
	(-12,1),(-12,2),(-12,3),(-12,4),(-12,5),(-12,6),(-12,7),(-12,8),(-12,9),(-12,10),(-11,-12),(-11,-11),
	(-11,-10),(-11,-9),(-11,-8),(-11,-7),(-11,-6),(-11,-5),(-11,-4),(-11,-3),(-11,-2),(-11,-1),(-11,0),
	(-11,1),(-11,2),(-11,3),(-11,4),(-11,5),(-11,6),(-11,7),(-11,8),(-11,9),(-11,10),(-10,-12),(-10,-11),
	(-10,-10),(-10,-9),(-10,-8),(-10,-7),(-10,-6),(-10,-5),(-10,-4),(-10,-3),(-10,-2),(-10,-1),(-10,0),
	(-10,1),(-10,2),(-10,3),(-10,4),(-10,5),(-10,6),(-10,7),(-10,8),(-10,9),(-10,10),(-9,-12),(-9,-11),
	(-9,-10),(-9,-9),(-9,-8),(-9,-7),(-9,-6),(-9,-5),(-9,-4),(-9,-3),(-9,-2),(-9,-1),(-9,0),(-9,1),(-9,2),
	(-9,3),(-9,4),(-9,5),(-9,6),(-9,7),(-9,8),(-9,9),(-9,10),(-8,-12),(-8,-11),(-8,-10),(-8,-9),(-8,-8),
	(-8,-7),(-8,-6),(-8,-5),(-8,-4),(-8,-3),(-8,-2),(-8,-1),(-8,0),(-8,1),(-8,2),(-8,3),(-8,4),(-8,5),
	(-8,6),(-8,7),(-8,8),(-8,9),(-8,10),(-7,-13),(-7,-12),(-7,-11),(-7,-10),(-7,-9),(-7,-8),(-7,-7),
	(-7,-6),(-7,-5),(-7,-4),(-7,-3),(-7,-2),(-7,-1),(-7,0),(-7,1),(-7,2),(-7,3),(-7,4),(-7,5),(-7,6),
	(-7,7),(-7,8),(-7,9),(-7,10),(-6,-13),(-6,-12),(-6,-11),(-6,-10),(-6,-9),(-6,-8),(-6,-7),(-6,-6),
	(-6,-5),(-6,-4),(-6,-3),(-6,-2),(-6,-1),(-6,0),(-6,1),(-6,2),(-6,3),(-6,4),(-6,5),(-6,6),(-6,7),
	(-6,8),(-6,9),(-6,10),(-5,-13),(-5,-12),(-5,-11),(-5,-10),(-5,-9),(-5,-8),(-5,-7),(-5,-6),(-5,-5),
	(-5,-4),(-5,-3),(-5,-2),(-5,-1),(-5,0),(-5,1),(-5,2),(-5,3),(-5,4),(-5,5),(-5,6),(-5,7),(-5,8),
	(-5,9),(-5,10),(-4,-14),(-4,-13),(-4,-12),(-4,-11),(-4,-10),(-4,-9),(-4,-8),(-4,-7),(-4,-6),(-4,-5),
	(-4,-4),(-4,-3),(-4,-2),(-4,-1),(-4,0),(-4,1),(-4,2),(-4,3),(-4,4),(-4,5),(-4,6),(-4,7),(-4,8),(-4,9),
	(-4,10),(-3,-13),(-3,-12),(-3,-11),(-3,-10),(-3,-9),(-3,-8),(-3,-7),(-3,-6),(-3,-5),(-3,-4),(-3,-3),
	(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),(-3,4),(-3,5),(-3,6),(-3,7),(-3,8),(-3,9),(-3,10),(-3,11),
	(-2,-13),(-2,-12),(-2,-11),(-2,-10),(-2,-9),(-2,-8),(-2,-7),(-2,-6),(-2,-5),(-2,5),(-2,6),(-2,7),(-2,8),
	(-2,9),(-2,10),(-2,11),(-1,-14),(-1,-13),(-1,-12),(-1,-11),(-1,-10),(-1,-9),(-1,6),(-1,7),(-1,8),(-1,9),
	(-1,10),(-1,11),(0,-14),(0,-13),(0,-12),(0,-11),(0,7),(0,8),(0,9),(0,10),(0,11),(1,-14),(1,-13),(1,-12),
	(1,8),(1,9),(1,10),(1,11),(2,-14),(2,-13),(2,9),(2,10),(3,10)
 }}dose[i,j])*(0.00179856115) <= max_s;
 

subject to const_3:(sum {(i,j) in {(-8,-35),(-8,-34),(-8,-33),(-8,-32),(-8,-31),(-7,-37),(-7,-36),
	(-7,-35),(-7,-34),(-7,-33),(-7,-32),(-7,-31),(-7,-30),(-7,-29),(-6,-39),(-6,-38),(-6,-37),
	(-6,-36),(-6,-35),(-6,-34),(-6,-33),(-6,-32),(-6,-31),(-6,-30),(-6,-29),(-6,-28),(-6,-27),
	(-5,-40),(-5,-39),(-5,-38),(-5,-37),(-5,-36),(-5,-35),(-5,-34),(-5,-33),(-5,-32),(-5,-31),
	(-5,-30),(-5,-29),(-5,-28),(-5,-27),(-5,-26),(-4,-41),(-4,-40),(-4,-39),(-4,-38),(-4,-37),
	(-4,-36),(-4,-35),(-4,-34),(-4,-33),(-4,-32),(-4,-31),(-4,-30),(-4,-29),(-4,-28),(-4,-27),
	(-4,-26),(-3,-41),(-3,-40),(-3,-39),(-3,-38),(-3,-37),(-3,-36),(-3,-35),(-3,-34),(-3,-33),
	(-3,-32),(-3,-31),(-3,-30),(-3,-29),(-3,-28),(-3,-27),(-3,-26),(-3,-25),(-2,-42),(-2,-41),
	(-2,-40),(-2,-39),(-2,-38),(-2,-37),(-2,-36),(-2,-35),(-2,-34),(-2,-33),(-2,-32),(-2,-31),
	(-2,-30),(-2,-29),(-2,-28),(-2,-27),(-2,-26),(-2,-25),(-1,-42),(-1,-41),(-1,-40),(-1,-39),
	(-1,-38),(-1,-37),(-1,-36),(-1,-35),(-1,-34),(-1,-33),(-1,-32),(-1,-31),(-1,-30),(-1,-29),
	(-1,-28),(-1,-27),(-1,-26),(-1,-25),(0,-43),(0,-42),(0,-41),(0,-40),(0,-39),(0,-38),(0,-37),
	(0,-36),(0,-35),(0,-34),(0,-33),(0,-32),(0,-31),(0,-30),(0,-29),(0,-28),(0,-27),(0,-26),
	(0,-25),(0,-24),(1,-43),(1,-42),(1,-41),(1,-40),(1,-39),(1,-38),(1,-37),(1,-36),(1,-35),
	(1,-34),(1,-33),(1,-32),(1,-31),(1,-30),(1,-29),(1,-28),(1,-27),(1,-26),(1,-25),(1,-24),
	(2,-43),(2,-42),(2,-41),(2,-40),(2,-39),(2,-38),(2,-37),(2,-36),(2,-35),(2,-34),(2,-33),
	(2,-32),(2,-31),(2,-30),(2,-29),(2,-28),(2,-27),(2,-26),(2,-25),(2,-24),(3,-43),(3,-42),
	(3,-41),(3,-40),(3,-39),(3,-38),(3,-37),(3,-36),(3,-35),(3,-34),(3,-33),(3,-32),(3,-31),
	(3,-30),(3,-29),(3,-28),(3,-27),(3,-26),(3,-25),(3,-24),(4,-43),(4,-42),(4,-41),(4,-40),
	(4,-39),(4,-38),(4,-37),(4,-36),(4,-35),(4,-34),(4,-33),(4,-32),(4,-31),(4,-30),(4,-29),
	(4,-28),(4,-27),(4,-26),(4,-25),(4,-24),(5,-42),(5,-41),(5,-40),(5,-39),(5,-38),(5,-37),
	(5,-36),(5,-35),(5,-34),(5,-33),(5,-32),(5,-31),(5,-30),(5,-29),(5,-28),(5,-27),(5,-26),
	(5,-25),(5,-24),(6,-42),(6,-41),(6,-40),(6,-39),(6,-38),(6,-37),(6,-36),(6,-35),(6,-34),
	(6,-33),(6,-32),(6,-31),(6,-30),(6,-29),(6,-28),(6,-27),(6,-26),(6,-25),(7,-41),(7,-40),
	(7,-39),(7,-38),(7,-37),(7,-36),(7,-35),(7,-34),(7,-33),(7,-32),(7,-31),(7,-30),(7,-29),
	(7,-28),(7,-27),(7,-26),(7,-25),(8,-40),(8,-39),(8,-38),(8,-37),(8,-36),(8,-35),(8,-34),
	(8,-33),(8,-32),(8,-31),(8,-30),(8,-29),(8,-28),(8,-27),(8,-26),(9,-39),(9,-38),(9,-37),
	(9,-36),(9,-35),(9,-34),(9,-33),(9,-32),(9,-31),(9,-30),(9,-29),(9,-28),(9,-27),(10,-38),
	(10,-37),(10,-36),(10,-35),(10,-34),(10,-33),(10,-32),(10,-31),(10,-30),(10,-29),(10,-28),
	(11,-36),(11,-35),(11,-34),(11,-33),(11,-32),(11,-31),(11,-30)
}} dose[i,j])*(0.00321543408) <= max_s;

subject to const_4:(sum {(i,j) in {(-7,28),(-7,29),(-7,30),(-7,31),(-7,32),(-7,33),(-6,27),(-6,28),
	(-6,29),(-6,30),(-6,31),(-6,32),(-6,33),(-6,34),(-5,25),(-5,26),(-5,27),(-5,28),(-5,29),
	(-5,30),(-5,31),(-5,32),(-5,33),(-5,34),(-5,35),(-5,36),(-4,24),(-4,25),(-4,26),(-4,27),
	(-4,28),(-4,29),(-4,30),(-4,31),(-4,32),(-4,33),(-4,34),(-4,35),(-4,36),(-4,37),(-3,23),
	(-3,24),(-3,25),(-3,26),(-3,27),(-3,28),(-3,29),(-3,30),(-3,31),(-3,32),(-3,33),(-3,34),
	(-3,35),(-3,36),(-3,37),(-2,22),(-2,23),(-2,24),(-2,25),(-2,26),(-2,27),(-2,28),(-2,29),
	(-2,30),(-2,31),(-2,32),(-2,33),(-2,34),(-2,35),(-2,36),(-2,37),(-2,38),(-1,22),(-1,23),
	(-1,24),(-1,25),(-1,26),(-1,27),(-1,28),(-1,29),(-1,30),(-1,31),(-1,32),(-1,33),(-1,34),
	(-1,35),(-1,36),(-1,37),(-1,38),(0,22),(0,23),(0,24),(0,25),(0,26),(0,27),(0,28),(0,29),
	(0,30),(0,31),(0,32),(0,33),(0,34),(0,35),(0,36),(0,37),(0,38),(0,39),(1,21),(1,22),(1,23),
	(1,24),(1,25),(1,26),(1,27),(1,28),(1,29),(1,30),(1,31),(1,32),(1,33),(1,34),(1,35),(1,36),
	(1,37),(1,38),(1,39),(2,21),(2,22),(2,23),(2,24),(2,25),(2,26),(2,27),(2,28),(2,29),(2,30),
	(2,31),(2,32),(2,33),(2,34),(2,35),(2,36),(2,37),(2,38),(2,39),(3,21),(3,22),(3,23),(3,24),
	(3,25),(3,26),(3,27),(3,28),(3,29),(3,30),(3,31),(3,32),(3,33),(3,34),(3,35),(3,36),(3,37),
	(3,38),(3,39),(4,21),(4,22),(4,23),(4,24),(4,25),(4,26),(4,27),(4,28),(4,29),(4,30),(4,31),
	(4,32),(4,33),(4,34),(4,35),(4,36),(4,37),(4,38),(4,39),(5,21),(5,22),(5,23),(5,24),(5,25),
	(5,26),(5,27),(5,28),(5,29),(5,30),(5,31),(5,32),(5,33),(5,34),(5,35),(5,36),(5,37),(5,38),
	(6,21),(6,22),(6,23),(6,24),(6,25),(6,26),(6,27),(6,28),(6,29),(6,30),(6,31),(6,32),(6,33),
	(6,34),(6,35),(6,36),(6,37),(6,38),(7,22),(7,23),(7,24),(7,25),(7,26),(7,27),(7,28),(7,29),
	(7,30),(7,31),(7,32),(7,33),(7,34),(7,35),(7,36),(7,37),(8,23),(8,24),(8,25),(8,26),(8,27),
	(8,28),(8,29),(8,30),(8,31),(8,32),(8,33),(8,34),(8,35),(8,36),(9,24),(9,25),(9,26),(9,27),
	(9,28),(9,29),(9,30),(9,31),(9,32),(9,33),(9,34),(9,35),(9,36),(10,25),(10,26),(10,27),
	(10,28),(10,29),(10,30),(10,31),(10,32),(10,33),(10,34),(10,35),(11,27),(11,28),(11,29),
	(11,30),(11,31),(11,32),(11,33),(11,34)}}
 dose[i,j])*(0.00355871886) <= max_s;

subject to const_5:(sum {(i,j) in {(19,-4),(19,-3),(19,-2),(19,-1),(19,0),(20,-7),(20,-6),(20,-5),
	(20,-4),(20,-3),(20,-2),(20,-1),(20,0),(20,1),(20,2),(21,-8),(21,-7),(21,-6),(21,-5),
	(21,-4),(21,-3),(21,-2),(21,-1),(21,0),(21,1),(21,2),(21,3),(22,-9),(22,-8),(22,-7),
	(22,-6),(22,-5),(22,-4),(22,-3),(22,-2),(22,-1),(22,0),(22,1),(22,2),(22,3),(22,4),
	(23,-10),(23,-9),(23,-8),(23,-7),(23,-6),(23,-5),(23,-4),(23,-3),(23,-2),(23,-1),(23,0),
	(23,1),(23,2),(23,3),(24,-10),(24,-9),(24,-8),(24,-7),(24,-6),(24,-5),(24,-4),(24,-3),
	(24,-2),(24,-1),(24,0),(24,1),(24,2),(24,3),(24,4),(25,-10),(25,-9),(25,-8),(25,-7),(25,-6),
	(25,-5),(25,-4),(25,-3),(25,-2),(25,-1),(25,0),(25,1),(25,2),(25,3),(25,4),(26,-11),(26,-10),
	(26,-9),(26,-8),(26,-7),(26,-6),(26,-5),(26,-4),(26,-3),(26,-2),(26,-1),(26,0),(26,1),(26,2),
	(26,3),(27,-11),(27,-10),(27,-9),(27,-8),(27,-7),(27,-6),(27,-5),(27,-4),(27,-3),(27,-2),
	(27,-1),(27,0),(27,1),(27,2),(27,3),(28,-11),(28,-10),(28,-9),(28,-8),(28,-7),(28,-6),
	(28,-5),(28,-4),(28,-3),(28,-2),(28,-1),(28,0),(28,1),(28,2),(28,3),(29,-11),(29,-10),
	(29,-9),(29,-8),(29,-7),(29,-6),(29,-5),(29,-4),(29,-3),(29,-2),(29,-1),(29,0),(29,1),
	(29,2),(30,-10),(30,-9),(30,-8),(30,-7),(30,-6),(30,-5),(30,-4),(30,-3),(30,-2),(30,-1),
	(30,0),(30,1),(30,2),(31,-9),(31,-8),(31,-7),(31,-6),(31,-5),(31,-4),(31,-3),(31,-2),
	(31,-1),(31,0),(31,1),(31,2),(32,-8),(32,-7),(32,-6),(32,-5),(32,-4),(32,-3),(32,-2),
	(32,-1),(32,0),(32,1),(33,-7),(33,-6),(33,-5),(33,-4),(33,-3),(33,-2),(33,-1),(33,0)
}} dose[i,j])*(0.00534759358) <= max_s;

#--------------------------------------------------------
#we want to use the second one when we use many angles.
#subject to l1odm{angle in ANGLES}:rad[angle,-max_odm] + rad[angle,max_odm] + sum{off in {-max_odm+1..max_odm}}t2[angle,off] <= 2*max_rad;

minimize amount:
	( sum {angle in ANGLES, off in {-max_odm+1..max_odm}} t2[angle,off]) + ( sum {angle in ANGLES} (rad[angle,-max_odm] + rad[angle,max_odm])) ;

#repeat{
solve;
#}	

#   printf "%7s: (", "Offset";
#   for {offset in -25..25} {
#     printf "%7.2f, ",offset;
#     }
#    printf ")\n";

# for {angle in ANGLES} {
#   printf "%7.2f: (", angle;
#   for {offset in -25..25} {
#     printf "%7.2f, ",rad[angle,offset];
#     }
#    printf ")\n";
# }

# printf "Dose: (";

# for {i in {-53..53}}{
#   printf "(";
#   for {j in {-75..75}}{
#       printf "%7.2f, ",dose[i,j];
#   }
#   printf "),\n";
# }

# printf ")\n";

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
var difference := 100;
var tmp_offset := -25;
set magic_set;
let magic_set := {};
var counter := 4;

repeat {
	for {i in {-25..24} diff magic_set} {
		if abs(rad[10,i] - rad[10,i+1]) <= 3 then {
			if abs(rad[10,i] - rad[10,i+1]) < difference then {
				let difference := abs(rad[10,i] - rad[10,i+1]);
				let tmp_offset := i;
			}
		}
	}
	let magic_set := magic_set union {tmp_offset};
	display difference;
	display tmp_offset;
	display magic_set;
	let counter := counter - 1;
	solve;
} until counter = 0;

subject to constMagic {i in magic_set}: rad[10,i] - rad[10,i+1] = 0;

#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------
#--------------------------------------------------------------------------


# param RHS{-25..24};
# let {i in -25..24} RHS[i] := 100;
	
# for {c in {-25..24}} {
# 	if abs(rad[10,c] - rad[10,c+1]) <= 2 then {
# 		 let RHS[c] := 0;
# 	}
# }
# #constUpper constrains that beamlet i - i+1 should be less than x[i]
# #
# subject to constUpper {i in -25..24}: rad[10,i] - rad[10,i+1] <= RHS[i];

# display RHS;
# solve;

#10, 50, 90, 130, 170, 200, 340


#print out offset labels
printf "%7s: (", "Offset";
for {offset in -25..25} {
	printf "%7.2f, ",offset;
}
printf ")\n";

#print out RHS values
# printf "%7s: (", "RHS";
# for {i in -25..24} {
# 	printf "%7.2f, ",RHS[i];
# }
# printf ")\n";	

for {i in -25..24} {
	printf "-----------";
}
printf "\n";

#print out beamlet values
for {angle in ANGLES} {
  printf "%7.2f: (", angle;
  for {offset in -25..25} {
    printf "%7.2f, ",rad[angle,offset];
    }
   printf ")\n";
}

printf "\n \n";

#print out Doses for all voxels
printf "Dose: (";
for {i in {-53..53}}{
  printf "(";
  for {j in {-75..75}}{
      printf "%7.2f, ",dose[i,j];
  }
  printf "),\n";
}

printf ")\n";

