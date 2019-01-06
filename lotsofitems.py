from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem,User

engine = create_engine('sqlite:///categories.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Alia Mohammed", email="alia55.m.j@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

#items for Candles1
Candles1 = Catalog(name = "Candles")

session.add(Candles1)
session.commit()

CatalogItem1 = CatalogItem(name = "FRESH BALSAM", description = "Woodland Balsam, Crisp Eucalyptus, Fir Branches, Cedarwood", categories = Candles1, user_id=1)

session.add(CatalogItem1)
session.commit()

CatalogItem2 = CatalogItem(name = "ICED VANILLA WOODS", description = "Iced Lavender, Sweet Vanilla, Ebony Wood", categories = Candles1,user_id=1)

session.add(CatalogItem2)
session.commit()

Candles2 = Catalog(name = "Candles2")

session.add(Candles2)
session.commit()

CatalogItem1 = CatalogItem(name = "FRESH BALSAM2", description = "Woodland Balsam, Crisp Eucalyptus, Fir Branches, Cedarwood", categories = Candles2, user_id=2)

session.add(CatalogItem1)
session.commit()

CatalogItem2 = CatalogItem(name = "ICED VANILLA WOODS2", description = "Iced Lavender, Sweet Vanilla, Ebony Wood", categories = Candles2, user_id=2)

session.add(CatalogItem2)
session.commit()



print "added catalog items!"
