export type CircuitDefinition = {
  id: string;
  displayName: string;
  aliases: string[];
  path: string;
};


const CURRENT_F1_2026_CIRCUITS: CircuitDefinition[] = [
  {
    id: "albert-park",
    displayName: "Albert Park",
    aliases: ["australia", "albert park", "melbourne"],
    path: "M 162 261 C 154 176 220 113 318 103 C 421 92 503 125 558 171 C 620 221 670 241 761 251 C 838 259 887 308 883 373 C 878 448 803 493 698 500 C 592 507 499 494 410 479 C 314 462 225 438 183 392 C 150 355 138 309 162 261 Z",
  },
  {
    id: "shanghai",
    displayName: "Shanghai International Circuit",
    aliases: ["china", "shanghai"],
    path: "M 164 190 C 171 120 252 86 347 102 C 441 119 482 174 476 240 C 470 307 401 335 315 331 C 260 328 214 349 206 393 C 199 433 227 469 296 480 C 384 495 486 474 578 443 C 665 413 739 373 804 379 C 853 383 886 415 887 462 C 888 511 845 543 770 544 C 678 545 596 507 518 483 C 434 458 367 455 291 451 C 194 446 127 392 126 316 C 124 265 157 236 164 190 Z",
  },
  {
    id: "suzuka",
    displayName: "Suzuka Circuit",
    aliases: ["japan", "suzuka"],
    path: "M 226 174 C 170 128 190 76 281 73 C 369 70 441 108 458 179 C 470 231 450 289 401 333 C 350 379 279 422 274 483 C 269 539 342 563 440 549 C 538 535 597 480 599 418 C 601 361 548 316 529 257 C 508 190 544 122 635 108 C 722 95 798 139 827 218 C 857 302 829 404 730 453 C 647 493 556 493 472 476 C 386 458 316 431 278 381 C 238 327 261 267 313 221 C 363 177 381 133 346 111 C 305 84 245 100 226 174 Z",
  },
  {
    id: "bahrain",
    displayName: "Bahrain International Circuit",
    aliases: ["bahrain", "sakhir"],
    path: "M 156 302 L 238 161 C 273 103 342 86 423 104 C 519 125 607 180 693 208 C 775 235 846 278 847 346 C 848 409 786 449 707 452 C 631 456 575 434 523 430 C 466 426 434 447 429 490 C 424 529 388 553 332 544 C 280 536 254 500 260 456 C 268 398 240 383 200 365 C 157 346 139 334 156 302 Z",
  },
  {
    id: "jeddah",
    displayName: "Jeddah Corniche Circuit",
    aliases: ["saudi", "jeddah"],
    path: "M 123 435 C 132 331 181 263 274 226 C 360 192 420 138 497 112 C 610 74 757 92 838 137 C 888 165 903 211 880 251 C 849 305 784 306 748 343 C 713 378 728 434 681 476 C 639 513 568 514 491 500 C 401 484 336 484 282 506 C 220 531 165 523 133 484 C 120 468 116 452 123 435 Z",
  },
  {
    id: "miami",
    displayName: "Miami International Autodrome",
    aliases: ["miami"],
    path: "M 178 161 L 729 159 C 800 159 844 194 844 255 L 843 371 C 842 438 797 474 720 474 L 327 474 C 252 474 205 444 206 390 C 207 349 245 322 303 319 L 494 314 C 545 314 574 294 574 260 C 574 225 547 206 503 206 L 178 206 C 126 206 97 180 97 138 C 97 95 126 71 178 71 L 620 71",
  },
  {
    id: "montreal",
    displayName: "Circuit Gilles Villeneuve",
    aliases: ["canada", "montreal", "gilles villeneuve"],
    path: "M 156 359 C 146 287 184 227 266 190 C 349 152 463 141 553 161 C 649 182 719 167 786 186 C 846 203 878 246 876 298 C 874 349 839 387 777 400 C 712 414 671 435 658 473 C 642 521 595 544 514 541 C 430 537 360 512 295 472 C 217 424 165 416 156 359 Z",
  },
  {
    id: "monaco",
    displayName: "Circuit de Monaco",
    aliases: ["monaco", "monte carlo"],
    path: "M 211 445 C 165 406 154 337 187 281 C 219 228 283 207 337 220 C 401 235 430 222 451 175 C 476 122 526 96 594 108 C 654 118 696 153 702 204 C 706 236 681 254 649 262 C 612 272 606 299 641 321 C 702 359 751 379 765 430 C 779 481 747 523 672 530 C 590 539 517 514 460 474 C 416 444 378 430 333 449 C 285 468 244 473 211 445 Z",
  },
  {
    id: "barcelona",
    displayName: "Circuit de Barcelona-Catalunya",
    aliases: ["barcelona", "catalunya", "spain", "barcelona-catalunya"],
    path: "M 150 351 C 144 272 196 215 286 202 C 358 191 418 167 455 124 C 486 88 536 71 602 79 C 681 88 760 130 800 192 C 843 259 832 344 767 399 C 709 448 621 459 533 442 C 470 430 411 434 362 463 C 301 499 229 501 182 463 C 155 440 152 398 150 351 Z",
  },
  {
    id: "red-bull-ring",
    displayName: "Red Bull Ring",
    aliases: ["austria", "red bull ring", "spielberg"],
    path: "M 170 454 L 305 155 L 741 138 L 830 281 L 688 452 L 325 491 Z",
  },
  {
    id: "silverstone",
    displayName: "Silverstone Circuit",
    aliases: ["great britain", "britain", "silverstone", "united kingdom"],
    path: "M 120 313 C 127 227 197 176 307 176 C 415 176 476 136 550 108 C 653 70 757 92 811 157 C 851 205 847 257 806 292 C 764 328 690 331 648 356 C 602 385 602 430 644 459 C 687 489 695 530 639 547 C 561 572 480 549 411 517 C 344 487 281 465 210 449 C 144 434 114 389 120 313 Z",
  },
  {
    id: "spa",
    displayName: "Spa-Francorchamps",
    aliases: ["belgium", "spa", "francorchamps"],
    path: "M 157 445 C 131 360 154 265 229 209 C 311 147 410 121 496 100 C 599 75 695 92 760 149 C 832 213 852 316 804 395 C 761 468 676 512 579 523 C 496 532 425 512 370 474 C 313 436 270 420 225 439 C 189 454 167 464 157 445 Z",
  },
  {
    id: "hungaroring",
    displayName: "Hungaroring",
    aliases: ["hungary", "hungaroring"],
    path: "M 167 365 C 151 273 211 199 331 189 C 426 181 488 208 539 183 C 588 159 621 116 683 111 C 756 106 821 154 845 226 C 870 302 845 383 781 431 C 712 482 624 491 548 467 C 480 445 430 447 382 470 C 328 496 257 501 208 470 C 178 451 173 407 167 365 Z",
  },
  {
    id: "zandvoort",
    displayName: "Zandvoort",
    aliases: ["netherlands", "zandvoort", "dutch"],
    path: "M 193 435 C 150 391 135 317 165 255 C 199 183 274 139 352 137 C 420 136 472 166 501 213 C 523 248 535 286 571 299 C 611 313 648 287 686 253 C 739 207 798 203 839 246 C 884 293 880 374 824 434 C 770 493 693 515 612 514 C 543 513 499 491 440 470 C 376 448 344 457 294 479 C 255 496 220 483 193 435 Z",
  },
  {
    id: "monza",
    displayName: "Autodromo Nazionale Monza",
    aliases: ["monza", "italy", "autodromo nazionale monza"],
    path: "M 158 277 C 170 167 259 109 397 106 L 633 103 C 757 102 847 162 861 264 C 872 348 817 422 730 454 C 678 473 621 468 565 452 C 504 435 448 423 387 436 C 323 449 265 444 218 419 C 167 391 145 340 158 277 Z",
  },
  {
    id: "madrid",
    displayName: "Madrid Circuit",
    aliases: ["madrid", "espana", "españa", "spain"],
    path: "M 162 183 L 779 182 C 845 182 887 215 887 271 C 887 321 858 343 799 352 L 588 386 C 522 397 491 430 491 478 C 491 522 460 548 409 548 C 355 548 327 519 327 471 C 327 410 292 381 217 376 L 160 372 C 112 369 85 344 85 302 L 85 252 C 85 207 112 183 162 183 Z",
  },
  {
    id: "baku",
    displayName: "Baku City Circuit",
    aliases: ["azerbaijan", "baku"],
    path: "M 137 171 L 789 171 C 843 171 878 196 878 239 C 878 277 853 296 803 301 L 483 329 C 406 336 373 372 373 441 L 373 475 C 373 521 340 551 286 551 C 231 551 199 520 199 473 L 199 240 C 199 199 174 171 137 171 Z",
  },
  {
    id: "singapore",
    displayName: "Marina Bay Street Circuit",
    aliases: ["singapore", "marina bay"],
    path: "M 168 421 C 135 359 139 269 184 208 C 227 149 303 124 389 136 C 467 146 519 136 565 102 C 620 62 708 58 784 91 C 856 123 887 193 865 268 C 842 348 775 380 705 392 C 639 404 604 431 586 476 C 565 526 510 548 431 543 C 341 537 262 506 211 464 C 193 449 179 436 168 421 Z",
  },
  {
    id: "cota",
    displayName: "Circuit of the Americas",
    aliases: ["united states", "cota", "austin", "circuit of the americas"],
    path: "M 150 472 C 129 392 164 298 237 236 C 317 169 412 145 482 101 C 551 58 651 52 735 86 C 824 122 879 199 879 286 C 879 344 848 385 794 405 C 744 424 701 421 656 449 C 603 482 594 542 515 553 C 431 565 347 535 287 499 C 237 469 187 470 150 472 Z",
  },
  {
    id: "mexico-city",
    displayName: "Autodromo Hermanos Rodriguez",
    aliases: ["mexico", "mexico city", "hermanos rodriguez"],
    path: "M 157 174 L 777 174 C 847 174 887 211 887 275 L 887 355 C 887 421 845 457 774 457 L 430 457 C 371 457 337 477 337 516 C 337 548 308 568 264 568 C 216 568 188 541 188 496 L 188 322 C 188 288 168 268 137 263 C 104 258 87 240 87 211 C 87 186 110 174 157 174 Z",
  },
  {
    id: "interlagos",
    displayName: "Interlagos",
    aliases: ["brazil", "sao paulo", "interlagos"],
    path: "M 171 447 C 144 373 159 286 220 226 C 290 157 387 135 480 151 C 547 162 596 150 649 116 C 713 75 796 86 842 143 C 890 202 888 287 841 350 C 798 407 728 431 651 439 C 574 447 522 468 468 507 C 403 555 314 561 246 527 C 213 510 186 483 171 447 Z",
  },
  {
    id: "las-vegas",
    displayName: "Las Vegas Strip Circuit",
    aliases: ["las vegas", "vegas"],
    path: "M 146 173 L 805 173 C 857 173 889 200 889 245 L 889 431 C 889 477 856 503 803 503 L 407 503 C 350 503 320 476 320 427 L 320 361 C 320 321 287 294 237 294 L 146 294 C 99 294 72 268 72 226 L 72 240 C 72 197 99 173 146 173 Z",
  },
  {
    id: "lusail",
    displayName: "Lusail International Circuit",
    aliases: ["qatar", "lusail"],
    path: "M 171 405 C 140 346 139 260 192 204 C 253 139 343 121 425 125 C 513 129 569 111 624 81 C 702 38 802 57 854 121 C 904 182 903 277 852 349 C 811 407 747 437 675 443 C 595 449 545 465 494 500 C 432 543 343 557 266 529 C 219 511 189 459 171 405 Z",
  },
  {
    id: "yas-marina",
    displayName: "Yas Marina Circuit",
    aliases: ["abu dhabi", "yas marina"],
    path: "M 152 407 C 124 346 132 261 185 207 C 243 148 333 136 416 158 C 474 173 517 173 567 148 C 627 117 711 118 784 149 C 856 179 893 242 888 313 C 883 390 834 447 756 470 C 680 493 623 485 564 499 C 503 514 462 548 388 549 C 296 550 216 518 177 461 C 165 444 157 426 152 407 Z",
  },
  {
    id: "default",
    displayName: "F1 Circuit",
    aliases: [],
    path: "M 142 324 C 142 214 231 133 360 122 C 454 114 531 92 590 67 C 684 28 795 63 849 142 C 902 222 884 319 814 382 C 756 434 672 454 596 446 C 514 438 446 449 390 484 C 317 529 221 528 165 468 C 142 444 142 391 142 324 Z",
  },
];


function normalize(value: string) {
  return value
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}


export function getCircuitDefinition(trackName?: string | null): CircuitDefinition {
  const normalized = normalize(trackName ?? "");
  if (!normalized) {
    return CURRENT_F1_2026_CIRCUITS.at(-1)!;
  }

  const match = CURRENT_F1_2026_CIRCUITS.find((circuit) =>
    circuit.aliases.some((alias) => normalized.includes(normalize(alias))),
  );

  return match ?? CURRENT_F1_2026_CIRCUITS.at(-1)!;
}


export const current2026CircuitNames = CURRENT_F1_2026_CIRCUITS.filter((circuit) => circuit.id !== "default").map(
  (circuit) => circuit.displayName,
);
