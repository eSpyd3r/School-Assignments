public class CompositeShow implements Show, Iterable<Show>, Command {

	private List<Show> SHOWS = new ArrayList<>();
	

	public CompositeShow(Show... pShows) {
		if (pShows.length < 2 || pShows.length > 5) {
			throw new IllegalAccessException("Must be between 2 and 5 shows inclusively");
		}

		SHOWS.addAll(Arrays.asList(pShows));
	}

	public CompositeShow(CompositeShow pCompositeShow) {
		for (Show show : pCompositeShow.SHOWS) {
			SHOWS.add(show.copy())
		}
	}

	public String description() {
		StringBuilder fullDescription = new StringBuilder();
		for (Show show : SHOWS) {
			fullDescription.add(show.description());
			fullDescription.add(", ");
		}
		return fullDescription;
	}

	public int runningTime() {
		int totalRunningTime;
		for (Show show : SHOWS) {
			totalRunningTime += show.runningTime();
		}
		return totalRunningTime;

	}

	public CompositeShow copy() {
		return new CompositeShow(this);
	}

	@Override
	public Iterator<Show> iterator() {
		return SHOWS.iterator();
	}

	@Override
	public boolean equals(Object pObject) {
		if (pObject == null) {return false;}
		if (pObject == this) {return true;}
		if (pObject.getClass() != getClass()) {return false;}

		CompositeShow compareCompositeShow = (CompositeShow) pObject;
		return Objects.equals(SHOWS, compareCompositeShow.SHOWS);
	}

	public void add(Show pShow) {
		Shows.add(pShow);
	}

	@Override
	public int hashCode() { return Objects.hash(SHOWS)}

	public Command createAddCommand(Show pShow) {
		return new Command() {

			@Override
			public void execute() {
				add(pShow);
			}

			@Override
			public void undo() {
				SHOWS.remove(pShow)
			}
		};
	}

}


public interface Command {
	void execute();
	void undo();
}

public class Client {
	public Concert concert = new Concert("ImGay", "Me", "69Minutes");
	public Movie movie1 = new Movie("TheBigBadFucko", "6969", "6969");
	public Movie movie1Copy = new Movie(movie1);
	public CompositeShow compositeMovies = new CompositeShow(movie1, movie1Copy);
	public CompositeShow aCompositeShow = new CompositeShow(concert, compositeMovies);
}

public class IntroducedShow implements Show {
	private Show aShow;
	private String aSpeaker;
	private int aDuration;

	public IntroducedShow(Show pShow, String pSpeaker, int pDuration) {
		aShow = pShow;
		aSpeaker = pSpeaker;
		aDuration = pDuration;
	}


	public String description() {
		StringBuilder introducedDescription = new StringBuilder();
		introducedDescription.add(aShow.description());
		introducedDescription.add(" is being introduced by %s for %d minutes", aSpeaker, aDuration);

		return introducedDescription;

	}

	public int runningTime() {
		return aShow.runningTime + aDuration;
	}

	public IntroducedShow copy() {
		return new IntroducedShow(aShow.copy(), aSpeaker, aDuration);
	}

	@Override
	public boolean equals(Object pObject) {
		if (pObject == this) {return true;}
		if (pObject.getClass() != getClass()) { return false; }
		if (pObject == null) { return false; }

		IntroducedShow compareIntroducedShow = (IntroducedShow) pObject;
		return (Objects.equals(compareIntroducedShow.aShow, aShow) && Objects.equals(compareIntroducedShow.aSpeaker, aSpeaker) && Objects.equals(compareIntroducedShow.aDuration, aDuration));
		
	}	

	@Override
	public int hashCode() { return Objects.hash(aShow, aSpeaker, aDuration)}
}

public class DoubleBill implements Show{
	private Movie aMove1;
	private Movie aMovie2;


	@Override
	public DoubleBill(Movie pMovie1, Movie pMovie2) {
		aMovie1 = pMovie1;
		aMovie2 = pMovie2;
	}

	public DoubleBill(DoubleBill pDoubleBill) {
		aMovie1 = new Movie(pDoubleBill.aMovie1);
		aMovie2 = new Movie(pDoubleBill.aMovie2);

	}

	@Override 
	public String description() {
		return (pMovie1.description() + "and" + pMovie2.description());
	}

	@Override
	public int runningTime() {
		return aMovie1.runningTime() + aMovie2.runningTime();
	}

	@Override
	public DoubleBill copy() {
		return new DoubleBill(aMovie1.copy(), aMovie2.copy())
	}

	@Override
	public boolean equals(Object pObject) {
		if (pObject == null) { return false; }

		if (pObject == this) { return true; }

		if (pObject.getClass() != getClass()) { return false; }

		DoubleBill compareDoubleBill = (DoubleBill) pObject;
		return (Objects.equals(pObject.aMovie1, aMovie1) && Objects.equals(pObject.aMovie2, aMovie2));

	}

	@Override
	public int hashCode() {return Objects.hash(aMovie1, aMovie2)}
}


public class IntroducedShowTest {
	Movie someMove = new Movie("asdf", 2, 2);
	IntroducedShow someIntroducedShow = new IntroducedShow(someMove);

	@Test
	public void deepCopyTest() {
		assertNotSame(someIntroducedShow, someIntroducedShow.copy());
		assertEquals(someIntroducedShow, someIntroducedShow.copy());
	}
}





