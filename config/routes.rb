Rails.application.routes.draw do
  root :to => "user_data#index"
  resources :items_for_sales
  resources :user_messagings
  resources :product_descriptions
  resources :user_data
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
