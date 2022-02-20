class ProductDescriptionsController < ApplicationController
  before_action :set_product_description,
                only: %i[show edit update destroy]

  def index
    @q = ProductDescription.ransack(params[:q])
    @product_descriptions = @q.result(distinct: true).includes(:seller,
                                                               :items_for_sales, :user_messagings).page(params[:page]).per(10)
  end

  def show
    @user_messaging = UserMessaging.new
    @items_for_sale = ItemsForSale.new
  end

  def new
    @product_description = ProductDescription.new
  end

  def edit; end

  def create
    @product_description = ProductDescription.new(product_description_params)

    if @product_description.save
      message = "ProductDescription was successfully created."
      if Rails.application.routes.recognize_path(request.referer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
        redirect_back fallback_location: request.referer, notice: message
      else
        redirect_to @product_description, notice: message
      end
    else
      render :new
    end
  end

  def update
    if @product_description.update(product_description_params)
      redirect_to @product_description,
                  notice: "Product description was successfully updated."
    else
      render :edit
    end
  end

  def destroy
    @product_description.destroy
    message = "ProductDescription was successfully deleted."
    if Rails.application.routes.recognize_path(request.referer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
      redirect_back fallback_location: request.referer, notice: message
    else
      redirect_to product_descriptions_url, notice: message
    end
  end

  private

  def set_product_description
    @product_description = ProductDescription.find(params[:id])
  end

  def product_description_params
    params.require(:product_description).permit(:name_of_item, :description,
                                                :seller_id, :sale_address, :product_category, :product_image, :price, :sale_status)
  end
end
