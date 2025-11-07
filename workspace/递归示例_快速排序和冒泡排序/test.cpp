#include<stdio.h>
#include<math.h>
int main(){
    float a,b,c,s,area;
    printf_s("input a,b,c:");
    scanf("%f,%f,%f",&a,&b,&c);
    s=(a+b+c)/2;
    printf_s("a=%f,b=%f,c=%f\ns=%f",a,b,c,s);
    area=(float)sqrt(s*(s-a)*(s-b)*(s-c));
    printf_s("area=%f",area);
}