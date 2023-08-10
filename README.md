# japan_stock
日本株の情報を確認できるようにする

# 環境構築

## Homebrewのインストール
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

## Pythonのインストール
brew install python

## 環境変数の設定
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

## 仮想環境の作成　※今回の場合、デスクトップのjapan_stock内に仮装環境ディレクトリを作成したいため、japan_stock内に移動してから下記を実行する
python3 -m venv myenv
source myenv/bin/activate

## ターミナルの処理行の先頭に(仮装環境名が表示されていればOK)

## 仮装環境がアクティブな状態でインストール

python -m pip install --upgrade pip setuptools

pip install streamlit

pip install yfinance

pip install pandas-datareader

## streamlit実行
streamlit run app.py

## 仮装環境を閉じる場合
deactivate