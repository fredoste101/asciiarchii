#include "messages.h"


void sendToAlice(FinalMessage* fm)
{
	//Send it to alice, she deserves it
}

void sendToBob(FinalMessage* fm)
{
	//bob seems like the better guy honestly
}


void eventHappend()
{
	FinalMessage fm;
	sendToAlice(&fm);	
}


void anotherEventHappend()
{
	FinalMessage fm;
	sendToAlice(&fm);	
}

/*
 * Daisy process or thread
 */
void* Daisy(void* args)
{

}
