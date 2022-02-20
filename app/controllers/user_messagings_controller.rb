class UserMessagingsController < ApplicationController
  before_action :set_user_messaging, only: %i[show edit update destroy]

  def index
    @q = UserMessaging.ransack(params[:q])
    @user_messagings = @q.result(distinct: true).includes(:recipient,
                                                          :product).page(params[:page]).per(10)
  end

  def show; end

  def new
    @user_messaging = UserMessaging.new
  end

  def edit; end

  def create
    @user_messaging = UserMessaging.new(user_messaging_params)

    if @user_messaging.save
      message = "UserMessaging was successfully created."
      if Rails.application.routes.recognize_path(request.referer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
        redirect_back fallback_location: request.referer, notice: message
      else
        redirect_to @user_messaging, notice: message
      end
    else
      render :new
    end
  end

  def update
    if @user_messaging.update(user_messaging_params)
      redirect_to @user_messaging,
                  notice: "User messaging was successfully updated."
    else
      render :edit
    end
  end

  def destroy
    @user_messaging.destroy
    message = "UserMessaging was successfully deleted."
    if Rails.application.routes.recognize_path(request.referer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
      redirect_back fallback_location: request.referer, notice: message
    else
      redirect_to user_messagings_url, notice: message
    end
  end

  private

  def set_user_messaging
    @user_messaging = UserMessaging.find(params[:id])
  end

  def user_messaging_params
    params.require(:user_messaging).permit(:recipient_id, :sender_id,
                                           :message_data, :product_id)
  end
end
