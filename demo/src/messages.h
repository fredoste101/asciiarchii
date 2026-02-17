

/*
 * Greet someone politly
 */
typedef struct Greeting
{
	int id;
	char * message;
} Greeting;


/*
 * Signal from bob to alice
 */
typedef struct Signal
{
	int id;
	float someCalc;
} Signal;


/*
 * Message with data. savy?
 */
typedef struct MessageData
{
	int fileHandle; //Bcuz why not
} MessageData;


/*
 * One message to rule them all
 */
typedef struct FinalMessage
{
	unsigned int someNumber;
} FinalMessage;
