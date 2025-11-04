# Book 클래스 생성
class Book:
    # 제목, 저자, isbn, 출판연도 초기화
    def __init__(self, title, author, isbn, publication_year):
        # 언더바를 붙여 캡슐화
        self._title = title
        self._author = author
        self._isbn = isbn
        self._publication_year = publication_year
        self._is_available = True

    # @property 데코레이터를 사용하여 속성을 외부에서 변수처럼 접근하게 해줌
    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def isbn(self):
        return self._isbn

    @property
    def publication_year(self):
        return self._publication_year
    
    @property
    def is_available(self):
        return self._is_available

    # 책의 대출 가능 상태를 변경하는 메서드
    def _set_availability(self, status):
        self._is_available = status

    # 객체를 문자열로 표현할 때 호출되는 내장 메서드
    def __str__(self):
        status = "대출 가능" if self._is_available else "대출 중"
        return f"제목: {self.title}, 저자: {self.author}, 상태: {status}"

# Member 클래스 생성
class Member:
    # 회원ID, 이름
    def __init__(self, member_id, name):
        # 언더바를 붙여서 캡슐화
        self._member_id = member_id
        self._name = name
        self._borrowed_books = []

    # @property 데코레이터를 사용하여 속성을 외부에서 변수처럼 접근하게 해줌
    @property
    def member_id(self):
        return self._member_id

    @property
    def name(self):
        return self._name
    
    @property
    def borrowed_books(self):
        return self._borrowed_books

    # 도서 대출
    def _add_borrowed_book(self, book):
        self._borrowed_books.append(book)

    # 도서 반납
    def _remove_borrowed_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)
            return True
        return False
    
    # 객체를 문자열로 표현하는 메서드
    def __str__(self):
        return f"회원 ID: {self.member_id}, 이름: {self.name}"

# Library 메서드 생성
class Library:
    # 책과 회원 정보를 관리
    def __init__(self):
        # 언더바를 붙여 캡슐화
        self._books = {}
        self._members = {}
    
    # 도서 추가
    def add_book(self, book: Book):
        if book.title in self._books:
            print(f"이미 존재하는 도서입니다: {book.title}")
            return False
        self._books[book.title] = book
        print(f"'{book.title}' 도서가 추가되었습니다.")
        return True

    # 도서 삭제
    def remove_book(self, book_title):
        if book_title not in self._books:
            print(f"'{book_title}' 도서를 찾을 수 없습니다.")
            return False
        del self._books[book_title]
        print(f"'{book_title}' 도서가 삭제되었습니다.")
        return True

    # 도서 검색
    def search_book(self, query):
        print(f"- '{query}'에 대한 검색을 시작합니다.")
        found_books = [
            book for book in self._books.values() 
            if query in book.title or query in book.author or query in book.isbn
        ]
        if not found_books:
            print(f"'{query}'에 대한 검색 결과가 없습니다.")
        else:
            print(f"'{query}'에 대한 검색 결과:")
            for book in found_books:
                print(f"- {book}")
        return found_books

    # 회원 검색
    def register_member(self, member: Member):
        if member.member_id in self._members:
            print(f"이미 존재하는 회원입니다: {member.name}")
            return False
        self._members[member.member_id] = member
        print(f"'{member.name}' 회원이 등록되었습니다.")
        return True

    # 도서 대출
    def checkout(self, book_title, member_id):
        book = self._books.get(book_title)
        member = self._members.get(member_id)

        if not book:
            print(f"'{book_title}' 도서를 찾을 수 없습니다.")
            return False
        if not member:
            print(f"회원 ID '{member_id}'를 찾을 수 없습니다.")
            return False
        if not book.is_available:
            print(f"'{book_title}' 도서는 현재 대출 중입니다.")
            return False

        book._set_availability(False)
        member._add_borrowed_book(book)
        print(f"'{member.name}'님이 '{book_title}'을(를) 대출했습니다.")
        return True

    # 도서 반납
    def return_book(self, book_title, member_id):
        book = self._books.get(book_title)
        member = self._members.get(member_id)
        
        if not book or not member:
            print("도서 또는 회원 정보를 찾을 수 없습니다.")
            return False
        
        if member._remove_borrowed_book(book):
            book._set_availability(True)
            print(f"'{member.name}'님이 '{book_title}'을(를) 반납했습니다.")
            return True
        else:
            print(f"'{member.name}'님은 '{book_title}'을(를) 대출하지 않았습니다.")
            return False

    # 회원의 대출 현황 확인
    def check_member_borrowed_status(self, member_id):
        member = self._members.get(member_id)
        if not member:
            print(f"회원 ID '{member_id}'를 찾을 수 없습니다.")
            return
        
        print(f"[{member.name}님의 대출 현황]")
        if not member.borrowed_books:
            print("대출한 도서가 없습니다.")
        else:
            for book in member.borrowed_books:
                print(f"- {book.title} (저자: {book.author})")

print("\n>>> 도서관 시스템 초기화")
library = Library()
print("="*80)

print(">>> 1. 도서 추가")
book1 = Book("개미", "베르나르 베르베르", "978-1111111111", 1991)
book2 = Book("데미안", "헤르만 헤세", "978-8937461807", 1919)
book3 = Book("이기적 유전자", "리처드 도킨스", "978-8932312674", 1976)
book4 = Book("총, 균, 쇠", "제레드 다이아몬드", "978-8972913079", 1997)
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.add_book(book4)
print("="*80)

print(">>> 2. 회원 등록")
member1 = Member("M001", "이태수")
member2 = Member("M002", "삼태수")
member3 = Member("M003", "사태수")
library.register_member(member1)
library.register_member(member2)
library.register_member(member3)
print("="*80)

print(">>> 3. 도서 검색")
library.search_book("개미")
library.search_book("헤세")
library.search_book("유전자")
library.search_book("원피스")   # 없는 도서
print("="*80)

print(">>> 4. 도서 대출 및 반납")
library.checkout("개미", "M001")
library.check_member_borrowed_status("M001")
library.return_book("개미", "M001")
library.check_member_borrowed_status("M001")
print("-"*40)

library.checkout("데미안", "M002")
library.check_member_borrowed_status("M002")
library.return_book("데미안", "M002")
library.check_member_borrowed_status("M002")
print("-"*40)

library.checkout("총, 균, 쇠", "M003")
library.check_member_borrowed_status("M003")
library.return_book("총, 균, 쇠", "M003")
library.check_member_borrowed_status("M003")
print("="*80)