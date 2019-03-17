
const int input_len = 6;
const int input_pins[input_len] = {A0,A1,A2,A3,A4,A5};
int input_values[input_len] = {0,0,0,0,0,0};
int input_players[input_len] = {0,0,0,0,0,0};

void setup() {
  // put your setup code here, to run once:
  for (int i=0;i<input_len; i++){
    pinMode(input_pins[i], INPUT_PULLUP);
  }
  //pinMode(3, INPUT);
  Serial.begin(9600);
  //attachInterrupt(digitalPinToInterrupt(E1), myintr, CHANGE);
}

int color_ts[] = {90,140,250,700};
int color_len = 4;

int player_len = 3; //number of players
int player_pos[] = {9,9,9}; //initial position for players

int state_detect(float value){
  int state = 0;
  for (int i = 0; i < color_len; i = i + 1) {
    if (color_ts[i] < value){
      state ++;
    }
    else
      break;
    }
  return state;
}

void send_message(){
  for(int i = 0; i < player_len; i++)
    Serial.print(player_pos[i]);
    Serial.print(' ');
    Serial.println();
}

void send_values(int* list){
  for(int i = 0; i < input_len; i ++){
    Serial.print(list[i]);
    Serial.print(' ');  
  }
  Serial.println();
}

void reset_players(){
  for(int i=0; i< player_len; i++)
    player_pos[i] = 9;
}

void loop() {  
  reset_players();
  
  // put your main code here, to run repeatedly:
  for (int i=0; i< input_len; i++){
      float p = analogRead(input_pins[i]);
      input_values[i] = p;
      int state = state_detect(p);
      input_players[i] = state;
      if (state >0)
        player_pos[state-1] = i;
  }

  //send_values(input_values);
  //send_values(input_players);  
  send_message();
  //Serial.println();

  /*
  if (p1 < 90){
    state = 1;
  }
  else if (p1 > 90 && p1 < 400){
    state = 2;
  }
  else if (p1 > 400){
    state = 3;
  }
  else{
    state = 4;
  }
  */
  delay(700);

}
