from parsel import Selector
import requests
import datetime


class Scrapper:
	base_url = 'https://siac.ufba.br/'
	materias_aprovadas = []
	materias_cursando = []

	def __init__(self, cpf, senha):
		self.cpf = cpf
		self.senha = senha
		self.session = requests.Session()

	def login(self):
		url = self.base_url + '/SiacWWW/LogonSubmit.do'
		data = {'cpf': self.cpf,
				'senha': self.senha}
		response = self.session.post(url, data=data)
		selector = Selector(response.text)
		if selector.xpath("//td[@class='menu']/a[text()='Página Inicial']"):
			return True
		return False

	def scrap(self):
		url = self.base_url + '/SiacWWW/ConsultarComponentesCurricularesCursados.do'
		response = self.session.get(url)
		selector = Selector(response.text)

		self.cr = selector.xpath("//td[b[text()='CR:']]/text()").extract_first()
		self.matricula = selector.xpath("//td[b[text()='MATRÍCULA:']]/text()").extract_first()
		self.curso = selector.xpath("//td[b[text()='CURSO:']]/text()").extract_first()
		self.curriculo = selector.xpath("//td[b[text()='CURRÍCULO:']]/text()").extract_first()
		self.data_acesso = datetime.datetime.now()

		tabela = selector.xpath("//table[@class='corpoHistorico' and tr/th[text()='Componentes Curriculares']]")

		for item in tabela.xpath("./tr[td[text()='AP' or text()='DU' or text()='DI']]"):
			materia = item.xpath("./td/text()").extract()
			if materia[0] == '\xa0':
				materia.pop(0)
			self.materias_aprovadas.append({'nome': materia[1].strip(), 'codigo': materia[0].strip()})
	
		for item in tabela.xpath("./tr[td[last()][text()='--']]"):
			materia = item.xpath("./td/text()").extract()
			if materia[0] == '\xa0':
				materia.pop(0)
			self.materias_cursando.append({'nome': materia[1].strip(), 'codigo': materia[0].strip()})

	def show(self):
		print('CURSO: {}'.format(self.curso))
		print('CURRÍCULO: {}'.format(self.curriculo))
		print('MATRICULA: {}'.format(self.matricula))
		print('CR: {}'.format(self.cr))
		print()
		print('{:^60}'.format('MATERIAS APROVADAS'))
		for item in self.materias_aprovadas:
			print(item)
		print()
		print('{:^60}'.format('MATERIAS CURSANDO'))
		for item in self.materias_cursando:
			print(item)
		print('\nAcessado em {}'.format(self.data_acesso.strftime(format='%d/%m/%Y %H:%M:%S')))
