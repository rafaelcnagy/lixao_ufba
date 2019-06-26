Rails.application.routes.draw do
  get 'home/index'
  get 'user/index'
  devise_for :users

  root to: 'home#index'

  match '/student', to: 'student#index', via: :get, as: :student_index
  match '/student/new', to: 'student#create', via: :post
 end
