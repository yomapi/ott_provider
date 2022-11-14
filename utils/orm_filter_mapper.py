class QueryMapper:
    """
    service와 repository간의 의존성을 끊기 위해, 파라매터를 받아 orm filter로 바꿔주는 클래스입니다.
    """

    def __init__(self, field_name: str, operator: str, value: any) -> None:
        self.feild_name = field_name
        self.operator = operator
        self.value = value

    def query(self) -> dict:
        """
        저장된 파라매터를 이용하여, django 쿼리셋 생성을 위한 dict를 만듭니다.
        Model.objects.filter(**{QueryMapper.query()}) 와 같이 사용합니다.
        """
        operator_map = {
            "<=": "__gte",
            ">=": "__lte",
            "=": "",
        }
        operation = f"{self.feild_name}{operator_map[self.operator]}"
        return {operation: self.value}


class QueryMapprList:
    """
    QueryMapper여러개를 갖는 class 입니다.
    """

    def __init__(self, queries: list[QueryMapper]):
        self.queries = queries

    def query(self) -> dict:
        """
        저장한 쿼리들을 하나로 합쳐서 쿼리셋 생성을 위한 dict를 만듭니다.
        Model.objects.filter(**{QueryMapper.query()}) 와 같이 사용합니다.
        """
        params = dict()
        for query in self.queries:
            params = {**params, **query.query()}
        return params
