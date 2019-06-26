class StudentController < ApplicationController
  skip_before_action :verify_authenticity_token  
  def create
    cpf = params[:cpf]
    password = params[:password]

    exec("python3 siac_scrapper.py '#{cpf}' '#{password}'")
    json = JSON.parse(File.read("/home/vinicius/Documentos/rubyProj/#{cpf}.json"))

    puts json
  end
end
