from database import db


class Equipamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String)
    categoria = db.Column(db.String)
    valor_diario = db.Column(db.Float, nullable=False)
    em_uso = db.Column(db.Boolean, default=False)
    def to_dict(self):
        return{
        "id": self.id,
        "nome": self.nome,
        "descricao": self.descricao,
        "categoria": self.categoria,
        "valor_diario": self.valor_diario,
        "em_uso": self.em_uso}

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    cpf = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    def to_dict(self):
        return{
        "id": self.id,
        "nome": self.nome,
        "telefone": self.telefone,
        "cpf": self.cpf,
        "email": self.email,}


class Aluguel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    equipamento_id = db.Column(db.Integer, db.ForeignKey("equipamento.id"), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    valor_total = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return{
        "id": self.id,
        "cliente_id": self.cliente_id,
        "equipamento_id": self.equipamento_id,
        "data_inicio": self.data_inicio.isoformat(),
        "data_fim": self.data_fim.isoformat(),
        "ativo": self.ativo,
        "valor_total": self.valor_total,}