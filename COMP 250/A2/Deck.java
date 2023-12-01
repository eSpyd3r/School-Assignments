 /**
* Your name here: Ethan Lim
* Your McGill ID here: 261029610
**/
 package assignment2;
import java.util.Random;

public class Deck {
    public static String[] suitsInOrder = {"clubs", "diamonds", "hearts", "spades"};
    public static Random gen = new Random();

    public int numOfCards; // contains the total number of cards in the deck
    public Card head; // contains a pointer to the card on the top of the deck

    /* 
     * TODO: Initializes a assignment2.Deck object using the inputs provided
     */
    public Deck(int numOfCardsPerSuit, int numOfSuits) {
	if (numOfCardsPerSuit > 13 || numOfCardsPerSuit < 1 || numOfSuits < 1 || numOfSuits > 4) {
		throw new IllegalArgumentException("Impossible Rank or Suit assignment");
	}
	this.head = new PlayingCard("clubs", 1); //will always be head if more than 1 card in deck other than joker

	Joker redJoker = new Joker("red"); //always second to last
	Joker blackJoker = new Joker("black"); //always last

	redJoker.next = blackJoker;
	blackJoker.prev = redJoker;
	blackJoker.next = this.head; //circular = tail to head
	this.head.prev = blackJoker; //circular - head to tail
	this.numOfCards = 3;

	if (numOfCardsPerSuit == 1 && numOfSuits == 1) { //edge case for just 1 added card
		this.head.next = redJoker;
		redJoker.prev = this.head;
	}

	PlayingCard pointer_last = (PlayingCard) this.head;
	for (int each_suit = 1; each_suit <= numOfSuits; each_suit++){
		for (int each_rank = 1; each_rank <= numOfCardsPerSuit; each_rank++){
			if (each_suit == 1 && each_rank == 1) {
				continue; //since AC already exists
			}
			PlayingCard pointer_new_card = new PlayingCard(suitsInOrder[each_suit-1],each_rank);
			this.numOfCards += 1;

			pointer_new_card.prev = pointer_last;
			pointer_last.next = pointer_new_card;

			if (each_suit == numOfSuits && each_rank == numOfCardsPerSuit) {
				redJoker.prev = pointer_new_card; //The 'lastCardInDeck.next' is the redJoker, while redJoker.prev is lastCardInDeck
				pointer_new_card.next = redJoker;
			}
			pointer_last = pointer_new_card; //switch pointer values so that we can assign 'next' for the new card in next iteration.

		}
	}

    }

    /* 
     * TODO: Implements a copy constructor for assignment2.Deck using Card.getCopy().
     * This method runs in O(n), where n is the number of cards in d.
     */
    public Deck(Deck d) {
		if (d.head != null) {
			this.head = d.head.getCopy(); //creates copy of head of input function and assigns the copy to the new deck
			this.numOfCards = 1;

			Card pointerCopyDeck = this.head; //points to first card in new deck
			Card pointerInputD = d.head; //points to first card in input deck

			while (this.numOfCards <= d.numOfCards) {
				if (this.numOfCards != d.numOfCards) {
					pointerCopyDeck.next = pointerInputD.next.getCopy(); //next field of card in new deck is assigned to a copy from the input

					Card tmpCopyDeck = pointerCopyDeck; //placeholder for current pointer location - helpful to assign prev in the new copy
					pointerCopyDeck = pointerCopyDeck.next; //pointer advances to copied card created/assigned in line 74
					pointerCopyDeck.prev = tmpCopyDeck; //prev field in new card is assigned to the old pointer location/card. the previous pointer location now has both next and prev

					pointerInputD = pointerInputD.next; //pointer in input deck advances
					this.numOfCards += 1;

				} else { //on the last card to copy, need to make circular link to head instead of new copy
					pointerCopyDeck.next = this.head;
					this.head.prev = pointerCopyDeck;
					break;
				}

			}
			}
		else {
			this.head = null;
			this.numOfCards = 0;
		}

	}

    /*
     * For testing purposes we need a default constructor.
     */
    public Deck() {}

    /* 
     * TODO: Adds the specified card at the bottom of the deck. This 
     * method runs in $O(1)$. 
     */
    public void addCard(Card c) {
		if (this.numOfCards != 0) {
			Card secondToLast = this.head.prev; //what used to be the last card is now second to last

			this.head.prev = c; //since circular, prev for head points to the added card

			secondToLast.next = c; //what used to be the last card now has next that points to c

			c.prev = secondToLast; //prev of added card points to secondToLast
			c.next = this.head; //added card next points to the top of the deck (head)

			this.numOfCards += 1; //adds to num of cards since a card has been added
		}
		else {
			this.head = c;
			c.next = c;
			c.prev = c;
			this.numOfCards = 1;
		}
    }

    /*
     * TODO: Shuffles the deck using the algorithm described in the pdf. 
     * This method runs in O(n) and uses O(n) space, where n is the total 
     * number of cards in the deck.
     */
    public void shuffle() {
	if (this.numOfCards != 0) {
		Card[] shuffleArray = new Card[this.numOfCards];
		shuffleArray[0] = this.head;
		Card pointer = this.head;

		for (int i = 1; i < this.numOfCards; i++) { //copying each card into array, reading from the head
			shuffleArray[i] = pointer.next;
			pointer = pointer.next;
		}

		for (int i = (this.numOfCards - 1); i > 0; i--) { //Fisher-Yates Shuffling
			int randNum = gen.nextInt(i + 1); //generates random integer that satisfies 0 <= randNum <= i

			Card tmp = shuffleArray[i]; //rearranges values in array
			shuffleArray[i] = shuffleArray[randNum];
			shuffleArray[randNum] = tmp;
		}

		this.head = shuffleArray[0]; //head is clearly first element in shuffled array
		this.head.prev = shuffleArray[this.numOfCards - 1]; //head points to last element in array
		shuffleArray[this.numOfCards - 1].next = this.head; //last element in shuffle points to top

		for (int i = 0; i < (this.numOfCards - 1); i++) { //stops an index early to avoid nullPointerException
			shuffleArray[i].next = shuffleArray[i + 1];
			shuffleArray[i + 1].prev = shuffleArray[i];
		}
	}
	else {
		Card[] emptyShuffle = new Card[0];
		this.head = null;
	}
    }

    /*
     * TODO: Returns a reference to the joker with the specified color in 
     * the deck. This method runs in O(n), where n is the total number of 
     * cards in the deck. 
     */
    public Joker locateJoker(String color) {
	if (this.numOfCards == 0) {
		return null;
	}

	if (this.head instanceof Joker && color.equals(((Joker)this.head).redOrBlack)) { //edge case s.t. head is Joker
		return (Joker)this.head;
	}

	Card jokerPointer = this.head;
	for (int i = 1; i <= this.numOfCards; i++) {
		if (jokerPointer instanceof Joker) {
			Joker targetJoker = (Joker) jokerPointer;
			if (color.equals(targetJoker.redOrBlack)){
				return (Joker) jokerPointer;
			}
		}
		jokerPointer = jokerPointer.next;
	}
	return null; //if there are no jokers in the deck
    }

    /*
     * TODO: Moved the specified Card, p positions down the deck. You can 
     * assume that the input Card does belong to the deck (hence the deck is
     * not empty). This method runs in O(p).
     */
    public void moveCard(Card c, int p) {
	int iterations = 0;

	while (iterations < p) {
		Card cBelowBefore = c.next; //c was in between these nodes before being moved...
		Card cAboveBefore = c.prev;

		cBelowBefore.prev = cAboveBefore; //connecting the nodes that surrounded c originally
		cAboveBefore.next = cBelowBefore;

		Card cBelowAfter = cBelowBefore.next; //the card that is directly after c, once moved, is the card that was once after cBelowBefore

		c.prev =  cBelowBefore; //cBelowBefore can be thought of as cAboveAfter
		c.next = cBelowAfter;

		cBelowBefore.next = c; //now, cBelowBefore is above c after movement
		cBelowAfter.prev = c; //connects the card that was once below cBelowBefore to c

		iterations++;
	}
    }

    /*
     * TODO: Performs a triple cut on the deck using the two input cards. You 
     * can assume that the input cards belong to the deck and the first one is 
     * nearest to the top of the deck. This method runs in O(1)
     */
    public void tripleCut(Card firstCard, Card secondCard) {
	if (this.head == firstCard) {this.head = secondCard.next;} //if first card on top
	else if(this.head.prev == secondCard) {this.head = firstCard;} //if second card on bottom

	else {
		Card firstCardTopPivot = this.head;
		Card firstCardBottomPivot = firstCard.prev;

		Card secondCardTopPivot = secondCard.next;
		Card secondCardBottomPivot = this.head.prev;

		this.head = secondCardTopPivot; //establish new head
		secondCardBottomPivot.next = firstCard;
		firstCard.prev = secondCardBottomPivot;

		secondCard.next = firstCardTopPivot;
		firstCardTopPivot.prev = secondCard;

		this.head.prev = firstCardBottomPivot;
		firstCardBottomPivot.next = this.head;

	}
    }

    /*
     * TODO: Performs a count cut on the deck. Note that if the value of the 
     * bottom card is equal to a multiple of the number of cards in the deck, 
     * then the method should not do anything. This method runs in O(n).
     */
    public void countCut() {
	if (numOfCards != 0 && (this.head.prev.getValue() != (this.numOfCards-1)) && ((this.head.prev.getValue() % numOfCards) != 0)){
		if (this.head.prev.getValue() == 1) {//edge case for bottom card being Ace
			Card originalHead = this.head;
			Card newHeadLocationPrev = this.head.prev.prev;
			Card tail = originalHead.prev; //same as newHeadLocationNext

			this.head = originalHead.next; //linking new head
			this.head.prev = tail;
			tail.next = this.head;

			originalHead.next = tail;
			tail.prev = originalHead;

			newHeadLocationPrev.next = originalHead;
			originalHead.prev = newHeadLocationPrev;

		}

		else {
			Card originalHead = this.head; //this.head will be updated later. although it's location in the deck has moved, the head still points here...
			Card newHeadLocationPrev = this.head.prev.prev;
			Card tail = this.head.prev;

			//need to find the last card to move....

			Card endCardToMove = this.head;
			for (int i = 1; i < (this.head.prev.getValue() % this.numOfCards); i++) {
				endCardToMove = endCardToMove.next;
			}

			this.head = endCardToMove.next; //updating head after cut
			tail.next = this.head; //connecting tail to head
			this.head.prev = tail; //connecting head to tail

			newHeadLocationPrev.next = originalHead; //moving original head
			originalHead.prev = newHeadLocationPrev;

			endCardToMove.next = tail; //connecting endCardToMove to bottom
			tail.prev = endCardToMove;

		}
	}
    }

    /*
     * TODO: Returns the card that can be found by looking at the value of the 
     * card on the top of the deck, and counting down that many cards. If the 
     * card found is a Joker, then the method returns null, otherwise it returns
     * the Card found. This method runs in O(n).
     */
    public Card lookUpCard() {
	int cardsToCount = this.head.getValue();

	Card cardToLookUp = this.head;
	for (int i = 1; i <= cardsToCount; i++) {
		cardToLookUp = cardToLookUp.next;
	}
	if (cardToLookUp instanceof Joker) {
		return null;
	}
	return cardToLookUp;
    }

    /*
     * TODO: Uses the Solitaire algorithm to generate one value for the keystream 
     * using this deck. This method runs in O(n).
     */
    public int generateNextKeystreamValue() {
	int keyStreamValue = 0;
	boolean generate = true;

	while(generate) {
		Joker blackJoker = locateJoker("black");
		Joker redJoker = locateJoker("red");

		moveCard(redJoker,1); //step 1
		moveCard(blackJoker,2); //step 2

		Card findJokerPointer = this.head; //need to find which joker is first...
		boolean search = true;
		while(search) { //iterates through list to find first joker
			if (findJokerPointer instanceof Joker) {
				Joker firstJoker = (Joker) findJokerPointer;
				if (blackJoker.getColor().equals(firstJoker.getColor())) { //compares firstJoker color to black and red
					tripleCut(blackJoker, redJoker); //step 3, blackJoker first
				}
				else {
					tripleCut(redJoker, blackJoker); //step 3, redJoker first
				}
				search = false;
			}
			findJokerPointer = findJokerPointer.next; //advances pointer through list
		}

		countCut(); //step 4

		Card keyStreamCard = lookUpCard(); //step 5

		if (!(keyStreamCard == null)) {
			keyStreamValue = keyStreamCard.getValue();
			generate = false; //ends keyStreamValue generation once a valid value is achieved
		}
	}
	return keyStreamValue;
    }

    public abstract class Card { 
	public Card next;
	public Card prev;

	public abstract Card getCopy();
	public abstract int getValue();

    }

    public class PlayingCard extends Card {
	public String suit;
	public int rank;

	public PlayingCard(String s, int r) {
	    this.suit = s.toLowerCase();
	    this.rank = r;
	}

	public String toString() {
	    String info = "";
	    if (this.rank == 1) {
		//info += "Ace";
		info += "A";
	    } else if (this.rank > 10) {
		String[] cards = {"Jack", "Queen", "King"};
		//info += cards[this.rank - 11];
		info += cards[this.rank - 11].charAt(0);
	    } else {
		info += this.rank;
	    }
	    //info += " of " + this.suit;
	    info = (info + this.suit.charAt(0)).toUpperCase();
	    return info;
	}

	public PlayingCard getCopy() {
	    return new PlayingCard(this.suit, this.rank);   
	}

	public int getValue() {
	    int i;
	    for (i = 0; i < suitsInOrder.length; i++) {
		if (this.suit.equals(suitsInOrder[i]))
		    break;
	    }

	    return this.rank + 13*i;
	}

    }

    public class Joker extends Card{
	public String redOrBlack;

	public Joker(String c) {
	    if (!c.equalsIgnoreCase("red") && !c.equalsIgnoreCase("black")) 
		throw new IllegalArgumentException("Jokers can only be red or black"); 

	    this.redOrBlack = c.toLowerCase();
	}

	public String toString() {
	    //return this.redOrBlack + " Joker";
	    return (this.redOrBlack.charAt(0) + "J").toUpperCase();
	}

	public Joker getCopy() {
	    return new Joker(this.redOrBlack);
	}

	public int getValue() {
	    return numOfCards - 1;
	}

	public String getColor() {
	    return this.redOrBlack;
	}
    }

	public void printDeck()
	{
		if(numOfCards==1)
		{
			System.out.println("Card: " + head+". Value: " + head.getValue());
			return;
		}
		Card currentCard = head;
		System.out.println("Previous\tCurrent\t\t\tNext ");
		for(int cardIndex = 0; cardIndex < numOfCards; cardIndex++)
		{
			System.out.println(currentCard.prev + " <--------- " + currentCard + " ---------> " + currentCard.next + ", Values are: " +currentCard.prev.getValue() + " and " + currentCard.getValue() + " and " + currentCard.next.getValue());
			currentCard = currentCard.next;
		}

		System.out.println("Number of cards: " + numOfCards);
	}
}

