class UserMessagingsController < ApplicationController
  before_action :set_user_messaging, only: [:show, :edit, :update, :destroy]

  # GET /user_messagings
  def index
    @user_messagings = UserMessaging.all
  end

  # GET /user_messagings/1
  def show
  end

  # GET /user_messagings/new
  def new
    @user_messaging = UserMessaging.new
  end

  # GET /user_messagings/1/edit
  def edit
  end

  # POST /user_messagings
  def create
    @user_messaging = UserMessaging.new(user_messaging_params)

    if @user_messaging.save
      redirect_to @user_messaging, notice: 'User messaging was successfully created.'
    else
      render :new
    end
  end

  # PATCH/PUT /user_messagings/1
  def update
    if @user_messaging.update(user_messaging_params)
      redirect_to @user_messaging, notice: 'User messaging was successfully updated.'
    else
      render :edit
    end
  end

  # DELETE /user_messagings/1
  def destroy
    @user_messaging.destroy
    redirect_to user_messagings_url, notice: 'User messaging was successfully destroyed.'
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_user_messaging
      @user_messaging = UserMessaging.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def user_messaging_params
      params.require(:user_messaging).permit(:recipient_id, :sender_id, :message_data, :product_id)
    end
end
