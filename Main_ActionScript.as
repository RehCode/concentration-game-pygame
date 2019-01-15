package {
	import flash.display.Sprite;
	import flash.events.MouseEvent;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	public class Main extends Sprite {
		private var pickedTiles:Array = new Array();  
		private const NUMBER_OF_TILES:uint=20;
		private var pause_game:Timer;
		private var canPick:Boolean=true;
		public function Main() {
			const TILES_PER_ROW:uint=5;
			var tiles:Array=new Array();
			var tile:tile_movieclip;
			for (var i:uint=0; i<NUMBER_OF_TILES; i++) {
				tiles.push(i); // change
			}
			var swap,tmp:uint;
			for (i=NUMBER_OF_TILES-1; i>0; i--) {
				swap=Math.floor(Math.random()*i);
				tmp=tiles[i];
				tiles[i]=tiles[swap];
				tiles[swap]=tmp;
			}
			for (i=0; i<NUMBER_OF_TILES; i++) {
				tile=new tile_movieclip();
				addChild(tile);
				tile.cardType=tiles[i];
				tile.x=5+(tile.width+5)*(i%TILES_PER_ROW);
				tile.y=5+(tile.height+5)*(Math.floor(i/TILES_PER_ROW));
				tile.gotoAndStop(NUMBER_OF_TILES+1); // change
				tile.buttonMode=true;
				tile.addEventListener(MouseEvent.CLICK,onTileClicked);
			}
		}
		private function onTileClicked(e:MouseEvent) {
			if(canPick){
				var picked:tile_movieclip=e.currentTarget as tile_movieclip;
				if (pickedTiles.indexOf(picked)==-1) {
					pickedTiles.push(picked);
					picked.gotoAndStop(picked.cardType+1);
				}
				if (pickedTiles.length==2) {
					canPick=false;
					pause_game=new Timer(1000,1);
					pause_game.start();
					if (Math.floor(pickedTiles[0].cardType/2)==Math.floor(pickedTiles[1].cardType/2)) { // change
						pause_game.addEventListener(TimerEvent.TIMER_COMPLETE,removeTiles);
					} else {
						pause_game.addEventListener(TimerEvent.TIMER_COMPLETE,resetTiles);
					}
				}
			}
		}
		private function removeTiles(e:TimerEvent) {
			pause_game.removeEventListener(TimerEvent.TIMER_COMPLETE,removeTiles);
			pickedTiles[0].removeEventListener(MouseEvent.CLICK,onTileClicked);
			pickedTiles[1].removeEventListener(MouseEvent.CLICK,onTileClicked);
			removeChild(pickedTiles[0]);
			removeChild(pickedTiles[1]);
			pickedTiles = new Array();
			canPick = true;
		}
		private function resetTiles(e:TimerEvent) {
			pause_game.removeEventListener(TimerEvent.TIMER_COMPLETE,resetTiles);
			pickedTiles[0].gotoAndStop(NUMBER_OF_TILES+1); // change
			pickedTiles[1].gotoAndStop(NUMBER_OF_TILES+1); // change
			pickedTiles = new Array();
			canPick = true;
		}
	}
}