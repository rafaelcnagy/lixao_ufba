class StudentController < ApplicationController
  skip_before_action :verify_authenticity_token

  def create
    cpf = params[:cpf]
    password = params[:password]

    system("python3 siac_scrapper.py '#{cpf}' '#{password}'")
    file = File.read("/home/vinicius/Documentos/rubyProj/#{cpf}.json")
    json = JSON.parse(file)

    redirect_to "/student", json: json['matricula']
  end

  def index
    @son = params[:json].class
  end

end
