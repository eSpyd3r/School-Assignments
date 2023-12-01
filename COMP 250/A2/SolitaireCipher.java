
/**
* Your name here: Ethan Lim
* Your McGill ID here: 261029610
**/
package assignment2;
public class SolitaireCipher {
    public Deck key;

    public SolitaireCipher(Deck key) {
	this.key = new Deck(key); // deep copy of the deck
    }

    /* 
     * TODO: Generates a keystream of the given size
     */
    public int[] getKeystream(int size) {
    int[] keyStream = new int[size];
    for (int i = 0; i <= size - 1; i++) {

        keyStream[i] = key.generateNextKeystreamValue();
    }

	return keyStream;
    }

    /* 
     * TODO: Encodes the input message using the algorithm described in the pdf.
     */
    public String encode(String msg) {

	String msgUpper = msg.toUpperCase();
    String msgEncode = ""; //msg to encode
    String ciphertext = ""; //final encryption

    for (int i = 0; i < msg.length(); i++) { //removal of non-alphabetical characters
        if (msgUpper.charAt(i) <= 90 && msgUpper.charAt(i) >= 65) {
            msgEncode += msgUpper.charAt(i);
        }
    }
    int[] keyStream = getKeystream(msgEncode.length()); //keyStream for message about to be encrypted
    for (int i = 0; i < msgEncode.length(); i++)  {
        int shift = keyStream[i];
        int encCharPos = msgEncode.charAt(i) - 'A';
        int newCharPos =  (encCharPos + shift) % 26; //position of new char
        char charToAdd = (char) ('A' + newCharPos);
        ciphertext += charToAdd;
    }
	return ciphertext;
    }

    /* 
     * TODO: Decodes the input message using the algorithm described in the pdf.
     */
    public String decode(String msg) {

    String ciphertext = "";
    int[] keyStream = getKeystream(msg.length());
    for (int i = 0; i < msg.length(); i++)  {
        int shift = keyStream[i];
        int encCharPos = msg.charAt(i) - 'A';
        int newCharPos =  (encCharPos - shift) % 26; //position of new char
        if (newCharPos < 0){
            char charToAdd = (char) ('Z' + 1 +newCharPos );
            ciphertext += charToAdd;
        }
        else {
            char charToAdd = (char) ('A' + newCharPos);
            ciphertext += charToAdd;
        }

        }
        return ciphertext;
    }

}

