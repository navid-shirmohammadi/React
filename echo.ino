#include <stdio.h>
#include <string.h>

int buffer_size = 30;
char str[30]="\0";
int count = 0;

void setup() {
  Serial.begin(9600);
  
}

void refresh(){
  for(int i=0; i<buffer_size; i++)
    str[i]="\0";
  count = 0;

  Serial.println('#');
}

void loop() {
  char character;

  while(Serial.available()) {
      character = Serial.read();

      if(character == '!'){
        // do some commands

        // refresh buffer
        refresh(); 
        continue; 
      }
      
      str[count] = character;
      count += 1;

      // avoid buffer overflow
      if(count == (buffer_size-1))
        refresh();
      
      Serial.println(str);
  }

}
