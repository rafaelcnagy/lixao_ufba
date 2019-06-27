class StudentController < ApplicationController
  skip_before_action :verify_authenticity_token

  def index
    cpf = params[:cpf]
    password = params[:password]

    system("python3 siac_scrapper.py '#{cpf}' '#{password}'")
    file = File.read("/home/deploy/siac_data/#{cpf}.json")
    @json = JSON.parse(file)

    if @json.key?('ERRO')
      redirect_to root_path
    else    
      @student = Student.find_or_create_by(cpf: cpf, registry: @json['matricula'], name: @json['nome'])

      aux = []
      aux2 = []
      for x in @json['materias_cursando'] do
        aux.push x['turma']
        q = Subject.where(code: x['codigo']).ids
        aux2= aux2+q 
      end
      # Turmas que esta matriculado
      @classes_current = ClassSubject.where(number: aux, subject_id: aux2)

      aux = []
      for x in @json['materias_aprovadas'] do
        aux.push x['codigo']
      end
      # Disciplinas que não foi aprovado (incluindo as matérias que ele está matriculado)
      @subjects_remain = Subject.where.not(code: aux)

      @subjects_done = Subject.where(code: aux)

      aux = []
      for x in @subjects_remain do
        aux.push x.id
      end
      # Turmas das disciplinas das @subjects_remain
      @classes_remain = ClassSubject.where(subject_id: @subjects_remain)

    end
  end
end
