class Api::V1::ItemsForSalesController < Api::V1::GraphitiController
  def index
    items_for_sales = ItemsForSaleResource.all(params)
    respond_with(items_for_sales)
  end

  def show
    items_for_sale = ItemsForSaleResource.find(params)
    respond_with(items_for_sale)
  end

  def create
    items_for_sale = ItemsForSaleResource.build(params)

    if items_for_sale.save
      render jsonapi: items_for_sale, status: 201
    else
      render jsonapi_errors: items_for_sale
    end
  end

  def update
    items_for_sale = ItemsForSaleResource.find(params)

    if items_for_sale.update_attributes
      render jsonapi: items_for_sale
    else
      render jsonapi_errors: items_for_sale
    end
  end

  def destroy
    items_for_sale = ItemsForSaleResource.find(params)

    if items_for_sale.destroy
      render jsonapi: { meta: {} }, status: 200
    else
      render jsonapi_errors: items_for_sale
    end
  end
end
