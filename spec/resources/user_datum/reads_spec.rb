require 'rails_helper'

RSpec.describe UserDatumResource, type: :resource do
  describe 'serialization' do
    let!(:user_datum) { create(:user_datum) }

    it 'works' do
      render
      data = jsonapi_data[0]
      expect(data.id).to eq(user_datum.id)
      expect(data.jsonapi_type).to eq('user_data')
    end
  end

  describe 'filtering' do
    let!(:user_datum1) { create(:user_datum) }
    let!(:user_datum2) { create(:user_datum) }

    context 'by id' do
      before do
        params[:filter] = { id: { eq: user_datum2.id } }
      end

      it 'works' do
        render
        expect(d.map(&:id)).to eq([user_datum2.id])
      end
    end
  end

  describe 'sorting' do
    describe 'by id' do
      let!(:user_datum1) { create(:user_datum) }
      let!(:user_datum2) { create(:user_datum) }

      context 'when ascending' do
        before do
          params[:sort] = 'id'
        end

        it 'works' do
          render
          expect(d.map(&:id)).to eq([
            user_datum1.id,
            user_datum2.id
          ])
        end
      end

      context 'when descending' do
        before do
          params[:sort] = '-id'
        end

        it 'works' do
          render
          expect(d.map(&:id)).to eq([
            user_datum2.id,
            user_datum1.id
          ])
        end
      end
    end
  end

  describe 'sideloading' do
    # ... your tests ...
  end
end
