class ChangeStudentCpfToBigInt < ActiveRecord::Migration[5.2]
  def change
  	change_column :students, :cpf, :bigint
  end
end
