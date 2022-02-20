require 'rails_helper'

RSpec.describe "product_descriptions#show", type: :request do
  let(:params) { {} }

  subject(:make_request) do
    jsonapi_get "/api/v1/product_descriptions/#{product_description.id}", params: params
  end

  describe 'basic fetch' do
    let!(:product_description) { create(:product_description) }

    it 'works' do
      expect(ProductDescriptionResource).to receive(:find).and_call_original
      make_request
      expect(response.status).to eq(200)
      expect(d.jsonapi_type).to eq('product_descriptions')
      expect(d.id).to eq(product_description.id)
    end
  end
end
