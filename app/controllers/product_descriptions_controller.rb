class ProductDescriptionsController < ApplicationController
  before_action :set_product_description, only: [:show, :edit, :update, :destroy]

  # GET /product_descriptions
  def index
    @product_descriptions = ProductDescription.all
  end

  # GET /product_descriptions/1
  def show
    @user_messaging = UserMessaging.new
    @items_for_sale = ItemsForSale.new
  end

  # GET /product_descriptions/new
  def new
    @product_description = ProductDescription.new
  end

  # GET /product_descriptions/1/edit
  def edit
  end

  # POST /product_descriptions
  def create
    @product_description = ProductDescription.new(product_description_params)

    if @product_description.save
      message = 'ProductDescription was successfully created.'
      if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
        redirect_back fallback_location: request.referrer, notice: message
      else
        redirect_to @product_description, notice: message
      end
    else
      render :new
    end
  end

  # PATCH/PUT /product_descriptions/1
  def update
    if @product_description.update(product_description_params)
      redirect_to @product_description, notice: 'Product description was successfully updated.'
    else
      render :edit
    end
  end

  # DELETE /product_descriptions/1
  def destroy
    @product_description.destroy
    message = "ProductDescription was successfully deleted."
    if Rails.application.routes.recognize_path(request.referrer)[:controller] != Rails.application.routes.recognize_path(request.path)[:controller]
      redirect_back fallback_location: request.referrer, notice: message
    else
      redirect_to product_descriptions_url, notice: message
    end
  end


  private
    # Use callbacks to share common setup or constraints between actions.
    def set_product_description
      @product_description = ProductDescription.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def product_description_params
      params.require(:product_description).permit(:name_of_item, :description, :seller_id, :sale_address, :product_category, :product_image, :price, :sale_status)
    end
end
