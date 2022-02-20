class Api::V1::ProductDescriptionsController < Api::V1::GraphitiController
  def index
    product_descriptions = ProductDescriptionResource.all(params)
    respond_with(product_descriptions)
  end

  def show
    product_description = ProductDescriptionResource.find(params)
    respond_with(product_description)
  end

  def create
    product_description = ProductDescriptionResource.build(params)

    if product_description.save
      render jsonapi: product_description, status: 201
    else
      render jsonapi_errors: product_description
    end
  end

  def update
    product_description = ProductDescriptionResource.find(params)

    if product_description.update_attributes
      render jsonapi: product_description
    else
      render jsonapi_errors: product_description
    end
  end

  def destroy
    product_description = ProductDescriptionResource.find(params)

    if product_description.destroy
      render jsonapi: { meta: {} }, status: 200
    else
      render jsonapi_errors: product_description
    end
  end
end
