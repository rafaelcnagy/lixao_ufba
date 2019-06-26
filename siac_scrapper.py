from parsel import Selector
import requests
import datetime
from time import sleep
import json
import os
import sys

class Scrapper:
	base_url = 'https://siac.ufba.br'

	def __init__(self, cpf, senha, json_path='/home/deploy/siac_data'):
		self.cpf = cpf
		self.senha = senha
		self.session = requests.Session()
		self.json_path = json_path
		self.materias_aprovadas = []
		self.materias_cursando = []
		self.status = True

	def login(self, retries=3):
		url = self.base_url + '/SiacWWW/LogonSubmit.do'
		data = {'cpf': self.cpf,
				'senha': self.senha}
		response = self.try_request(method='POST', url=url, data=data)
		response.raise_for_status()
		selector = Selector(response.text)
		if selector.xpath("//td[@class='menu']/a[text()='Página Inicial']"):
			self.status = True
		else:
			self.status = False

	def scrap(self, retries=3):
		# Dados e matérias aprovadas
		if not self.status:
			return
		url = self.base_url + '/SiacWWW/ConsultarComponentesCurricularesCursados.do'
		response = self.try_request(method='GET', url=url)
		response.raise_for_status()
		selector = Selector(response.text)

		self.cr = selector.xpath("//td[b[text()='CR:']]/text()").extract_first().strip()
		self.matricula = selector.xpath("//td[b[text()='MATRÍCULA:']]/text()").extract_first().strip()
		self.curso = selector.xpath("//td[b[text()='CURSO:']]/text()").extract_first().strip()
		self.curriculo = selector.xpath("//td[b[text()='CURRÍCULO:']]/text()").extract_first().strip()
		self.data_acesso = datetime.datetime.now()

		tabela = selector.xpath("//table[@class='corpoHistorico' and tr/th[text()='Componentes Curriculares']]")

		if not tabela:
			raise Exception('Tabela1 não encontrada')
			self.status = False
			return

		for item in tabela.xpath("./tr[td[text()='AP' or text()='DU' or text()='DI']]"):
			materia = item.xpath("./td/text()").extract()
			if materia[0] == '\xa0':
				materia.pop(0)
			self.materias_aprovadas.append({'codigo': materia[0].strip(), 'nome': materia[1].strip()})

		# Matérias cursando

		url = self.base_url + '/SiacWWW/ConsultarComprovanteMatricula.do'
		response = self.try_request(method='GET', url=url)
		selector = Selector(response.text)

		tabela = selector.xpath("//table[@class='simple2'][1]")

		if not tabela:
			raise Exception('Tabela2 não encontrada')
			self.status = False
			return

		for item in tabela.xpath(".//tr[td[1][b]]"):
			materia = item.xpath("./td/b/text()").extract()
			self.materias_cursando.append({'codigo': materia[0].strip(), 'nome': materia[1].strip(), 'turma': materia[3].strip()})

		self.status = True

	def create_json(self):	
		if not os.path.exists(self.json_path):
			os.makedirs(self.json_path)
		with open(self.json_path + f'/{self.cpf}.json', mode='w', encoding='utf_8') as json_file:
			if self.status:
				json.dump({'curso': self.curso,
						   'curriculo': self.curriculo,
						   'matricula': self.matricula,
						   'cr': self.cr,
						   'materias_aprovadas': self.materias_aprovadas,
						   'materias_cursando': self.materias_cursando,
						   'data_acesso': self.data_acesso.strftime(format='%d/%m/%Y %H:%M:%S')},
						   json_file, ensure_ascii=False, indent=4)
			else: 
				json.dump({'ERRO': 'não foi possivel carregar informações',
						   'data_acesso': datetime.datetime.now().strftime(format='%d/%m/%Y %H:%M:%S')},
						   json_file, ensure_ascii=False, indent=4)

	def show(self):
		if not self.status:
			print('ERRO: Aluno não tem dados!')
			return
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

	def try_request(self, method='GET', url='', timeout=10, retry=3, headers=None, data=None):
		if not headers:
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
					   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					   'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5'}
		for i in range(retry):
			if method == 'POST':
				response = self.session.post(url=url, headers=headers, data=data, timeout=timeout)
			else:
				response = self.session.get(url=url, headers=headers, data=data, timeout=timeout)
			if int(response.status_code / 100) <= 2:
				return response
			else:
				print('Erro no request')
				sleep(60)
		print("Erro no request!")
		return None

cpf = sys.argv[1]
senha = sys.argv[2]
aluno = Scrapper(cpf, senha)
aluno.login()
aluno.scrap()
aluno.create_json()
