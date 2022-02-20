require 'rails_helper'

RSpec.describe "items_for_sales#show", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/items_for_sales/#{items_for_sale.id}", params: params
  end

  describe 'basic fetch' do
    let!(:items_for_sale) { create(:items_for_sale) }

    it 'works' do
      expect(ItemsForSaleResource).to receive(:find).and_call_original
      make_request
      expect(response.status).to eq(200)
      expect(d.jsonapi_type).to eq('items_for_sales')
      expect(d.id).to eq(items_for_sale.id)
    end
  end
end
