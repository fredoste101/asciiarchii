#include "messages.h"

void sendSignalToAlice(Signal* s)
{
	//Somehow send signal. 
}

void processGreeting(Greeting* g)
{
	//Do some processing
}

/*
 * Takes care of the greeting from alice
 */
void* handleHello(Greeting* g)
{
	processGreeting();

	Signal s;

	sendSignalToAlice(&s);

}


/*
 * A final message. Change the world.
 */
void finalMessageReceiver(FinalMessage* fm)
{
	//We got the final message! yeah!
}


/*
 * bob process or thread
 */
void Bob(void* args)
{


}
