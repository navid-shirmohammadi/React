#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int buffer_size = 30;
char str_x[30]="\0";
char str_y[30]="\0";
int count_x = 0;
int count_y = 0;


int X_RPWM = 3;
int X_LPWM = 5;
int Y_RPWM = 6;
int Y_LPWM = 9;

void setup() {
  Serial.begin(9600);
}

void refresh(){
  for(int i=0; i<buffer_size; i++)
    str_x[i]="\0";
    str_y[i]="\0";
    count_x = 0;
    count_y = 0;

  Serial.println('#');
}

void set_signal(){
    int pwm_x = atoi(str_x);
    int pwm_y = atoi(str_y);

    if(pwm_x>0){
      analogWrite(X_RPWM,0);   //Power Supply Current= 4.35A
      analogWrite(X_LPWM,pwm_x);   
    }
    else{
      analogWrite(X_RPWM,-pwm_x);   //Power Supply Current= 4.35A
      analogWrite(X_LPWM,0);   
    }


        if(pwm_y>0){
      analogWrite(Y_RPWM,0);   //Power Supply Current= 4.35A
      analogWrite(Y_LPWM,pwm_y);   
    }
    else{
      analogWrite(Y_RPWM,-pwm_y);   //Power Supply Current= 4.35A
      analogWrite(Y_LPWM,0);   
    }
      
}

void loop() {
  char character;
  bool reading_x = true;
  
  while(Serial.available()) {
      character = Serial.read();
    
      if(character == '?'){
        reading_x = false; 
      }

      else if (character == '!'){
        set_signal();
        refresh();
        continue;
      }

      else if(reading_x){
        str_x[count_x] = character;
        count_x += 1;
      }
      else{
        str_y[count_y] = character;
        count_y += 1;
      }
      
  }

}
