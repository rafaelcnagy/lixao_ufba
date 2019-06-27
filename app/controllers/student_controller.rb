class StudentController < ApplicationController
  skip_before_action :verify_authenticity_token

  def create
    cpf = params[:cpf]
    password = params[:password]

    system("python3 siac_scrapper.py '#{cpf}' '#{password}'")
    file = File.read("/home/deploy/siac_data/#{cpf}.json")
    @json = JSON.parse(file)

    student = Student.first_or_create(cpf: cpf, registry: @json['matricula'], name: @json['nome'])

    render :index
  end

  def index
    @sub = Subject.where.not(code: @json['materias_aprovadas']['codigo'])
  end

end
