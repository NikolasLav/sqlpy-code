import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import case_orm_config as db
import json

Base = declarative_base()


class Publisher(Base):
	__tablename__ = "publisher"
	id = sq.Column(sq.Integer, primary_key=True)
	name = sq.Column(sq.String(length=160), nullable=False)
	def __str__(self) -> str:
		return f'Издатель №{self.id}: {self.name}'


class Shop(Base):
	__tablename__ = "shop"
	id = sq.Column(sq.Integer, primary_key=True)
	name = sq.Column(sq.String(length=160), nullable=False)

	def __str__(self) -> str:
		return f'Магазин №{self.id}: {self.name}'


class Book(Base):
	__tablename__ = "book"
	id = sq.Column(sq.Integer, primary_key=True)
	title = sq.Column(sq.String(length=160), nullable=False)
	id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
	publisher = relationship(Publisher, backref="book")
	def __str__(self) -> str:
			return f'Книга №{self.id}: {self.title}, {self.id_publisher}'


class Stock(Base):
	__tablename__ = "stock"
	id = sq.Column(sq.Integer, primary_key=True)
	id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
	id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
	count = sq.Column(sq.Integer, nullable=False)
	book = relationship(Book, backref="stock")
	shop = relationship(Shop, backref="stock")


class Sale(Base):
	__tablename__ = "sale"
	id = sq.Column(sq.Integer, primary_key=True)
	price = sq.Column(sq.Float, nullable=False)
	date_sale = sq.Column(sq.Date, nullable=False)
	id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
	count = sq.Column(sq.Integer, nullable=False)
	stock = relationship(Stock, backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def add_publisher(id, name):
	publisher = Publisher(id=id, name=name)
	session.add(publisher)
	session.commit()


def add_shop(id, name):
	shop = Shop(id=id, name=name)
	session.add(shop)
	session.commit()


def add_book(id, title, id_publisher):
	book = Book(id=id, title=title, id_publisher=id_publisher)
	session.add(book)
	session.commit()


def add_stock(id, id_shop, id_book, count):
	stock = Stock(id=id, id_shop=id_shop, id_book=id_book, count=count)
	session.add(stock)
	session.commit()


def add_sale(id, price, date_sale, count, id_stock):
	sale = Sale(id=id, price=float(price), datesale=date_sale, count=count, id_stock=id_stock)
	session.add(sale)
	session.commit()


def take_data():
	with open('fixtures/tests_data.json', encoding='utf-8') as new_file:
		data = json.load(new_file)
	for record in data:
		model = {
			'publisher': Publisher,
			'shop': Shop,
			'book': Book,
			'stock': Stock,
			'sale': Sale,
		}[record.get('model')]
		print(model(id=record.get('pk'), **record.get('fields')))
		# if item['model'] == 'publisher':
		# 	try:
		# 		add_publisher(item['pk'], item['fields']['name'])
		# 	except:
		# 		print('ошибка с добавлением объекта:', item)
		# if item['model'] == 'shop':
		# 	try:
		# 		add_shop(item['pk'], item['fields']['name'])
		# 	except:
		# 		print('ошибка с добавлением объекта:', item)
		# if item['model'] == 'book':
		# 	try:
		# 		add_book(item['pk'], item['fields']['title'], item['fields']['id_publisher'])
		# 	except:
		# 		print('ошибка с добавлением объекта:', item)
		# if item['model'] == 'stock':
		# 	try:
		# 		add_stock(item['pk'], item['fields']['id_shop'], item['fields']['id_book'], item['fields']['count'])
		# 	except:
		# 		print('ошибка с добавлением объекта:', item)
		# if item['model'] == 'sale':
		# 	try:
		# 		add_sale(item['pk'], item['fields']['price'], item['fields']['date_sale'], item['fields']['count'], item['fields']['id_stock'])
		# 	except:
		# 		print('ошибка с добавлением объекта:', item)


# def find_shop_by_publisher(publisher = input('Введите id или название издателя: ')):
# 	try:
# 		publisher=int(publisher)
# 		q = session.query(Shop.name).distinct(Shop.name).join(Stock).join(Book).filter(Book.id_publisher == publisher)

# 	except:
# 		q = session.query(Shop.name).distinct(Shop.name).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher)

# 	print('Магазины, в которых представлен издатель:')
# 	for s in q.all():
# 		print(*s)


# server, password, uri, port, db_name = db.settings.values()
# DSN = f"postgresql://{server}:{password}@{uri}:{port}/{db_name}"
# engine = sq.create_engine(DSN, echo=None)
# Session = sessionmaker(bind=engine)
# session = Session()

# create_tables(engine) #создаем таблицы в БД
take_data() #импортируем данные в БД из файла по заданию
# find_shop_by_publisher() # Выводит название магазинов (shop), в которых представлены книги конкретного издателя, получая имя или идентификатор издателя (publisher)