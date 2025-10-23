from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    def __repr__(self):
        cls = self.__class__.__name__
        pk = getattr(self, "id", None)
        return f"<{cls}(id={pk})>"

    id: Mapped[int] = mapped_column(primary_key=True)
