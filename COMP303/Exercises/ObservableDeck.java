public class ObservableDeck implements DeckView {
	private List<Card> aCards = new ArrayList<>();
	private List<Observer> aObservers = new ArrayList<>();
	private Card lastCardDrawn;

	public ObservableDeck() { shuffle(); }

	public void shuffle()
	{
		aCards.clear()
		for( Suit suit : Suit.values) {
			for( Rank rank : Rank.values) {
				aCards.add (new Card(rand, suit));

			}
		}
		Collections.shuffle(aCards);

		for (Observer observer : aObservers) {
			observer.shuffled();
		}
	}

	public void push(Card pCard) {
		aCards.add(pCard);
		for (Observer observer : aObservers) {
			observer.cardPushed(this);
		}
	}

	public Card draw() {
		Card card = aCards.remove(aCards.size() - 1);
		lastCardDrawn = card;
		for (Observer observer : aObservers) {
			observer.cardDrawn(this);
		}

		return card;
	}

	public boolean isEmpty() { return aCards.isEmpty(); }

	public List<Card> getCards() { return Collections.unmodifiableList(aCards);}

	public void addObserver(Observer pObserver) {
		aObservers.add(pOberver);
	}

	@Override
	public List<Card> getCards() {
		return Collections.unmodifiableList(aCards);
	}

	@Override
	public Card getLastCardDrawn() {
		return lastCardDrawn;
	}


	public void main(String[] args) {
		Observer drawLogger = new DrawLogger();
		Observer sizeStatus = new SizeStatus;
		Deck deck = new Deck();

		deck.addObserver(drawLogger);
		deck.addObserver(sizeStatus);

		Card drawnCard = deck.draw();

		deck.push(drawnCard);
	}
}

public interface DeckView {
	List<Card> getCards();
	Card getLastCardDrawn;
}

public interface Observer {
	void cardDrawn(Deck pDeck);
	void cardPushed(Deck pDeck);
	void shuffled():
}

abstract class ObserverAdapter implements Observer {
	@Override
	public void cardDrawn(DeckView pDeck){}

	@Override
	public void cardPushed(DeckView pDeck){}

	@Override 
	public void shuffled(){}
}



public class DrawLogger extends ObserverAdapter {
	public DrawLogger(){}

	@Override
	public void cardDrawn(DeckView pDeck) {
		System.out.println(pDeck.getLastCardDrawn());
	}
}

public class SizeStatus extends ObserverAdapter {
	private int currentSize = 52;

	public SizeStatus(){}

	@Override
	public void cardDrawn(DeckView pDeck) {
		System.out.println(pDeck.getCards().size())
	}

	@Override
	public void cardPushed(DeckView pDeck) {
		System.out.println(pDeck.getCards().size())
	}

	@Override
	public void shuffled() {
		System.out.println(52);
	}
}















