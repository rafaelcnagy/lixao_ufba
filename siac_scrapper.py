from parsel import Selector
import requests
import datetime
from time import sleep
import json

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
		#response = self.try_request(url)
		selector = Selector(response.text)

		self.cr = selector.xpath("//td[b[text()='CR:']]/text()").extract_first()
		self.matricula = selector.xpath("//td[b[text()='MATRÍCULA:']]/text()").extract_first()
		self.curso = selector.xpath("//td[b[text()='CURSO:']]/text()").extract_first()
		self.curriculo = selector.xpath("//td[b[text()='CURRÍCULO:']]/text()").extract_first()
		self.data_acesso = datetime.datetime.now()

		tabela = selector.xpath("//table[@class='corpoHistorico' and tr/th[text()='Componentes Curriculares']]")

		if not tabela:
			return False

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
		return True

	def create_json(self):
		with open('/%s.json' % self.matricula, 'w') as json_file:
			json.dumps({'curso': self.curso, 
					'curriculo':self.curriculo, 
					'matricula': self.matricula, 
					'cr': self.cr, 
					'materias_aprovadas': self.materias_aprovadas,
					'materias_cursando': self.materias_cursando,
					'data_acesso': self.data_acesso},
					json_file)

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

	def try_request(self, url, timeout=10, retry=3, headers=None, data=None):
		if not headers:
			headers = {	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
						'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
						'Accept-Encoding':	'gzip, deflate, br',
						'Accept-Language':	'en-US,en;q=0.5'}
		for i in range(retry):
			response = self.session.get(url=url, headers=headers, data=data, timeout=timeout)
			if int(response.status_code/100) == 1:
				return response
			else:
				print('Erro no request')
				sleep(60)
		print("Erro no request!")
		return None