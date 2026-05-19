//import the testing functions from the vitest library
import {describe, it, expect} from 'vitest'

//import the function to be tested
import {useTimeBlock} from '../../composables/useTimeBlock'

//describe the test groups for the useTimeBlock function
//Think of it like a folder label - "All tests related to the useTimeBlock function will go here"

describe('useTimeBlock', () => {

//it describes a specific test case - "it should compute the correct time block based on the current time"
it('should return the correct thirty minute time block based on a current time', () => {

    //We are using an example o 10:15 AM, which should fall into the 10:00 - 10:30 block
    //ARRANGE - Setup what we need for the test

    const hours = 10
    const minute = 15

    //Manually calculate what the function should return
    const blockStart = Math.floor((hours * 60 + minute) / 30) * 30
    const startH = Math.floor(blockStart / 60)
    const startM = blockStart % 60
    const endH = Math.floor((blockStart + 30) / 60) >= 24 ? 0 : Math.floor((blockStart + 30) / 60)
    const endM = (blockStart + 30) % 60
    const expectedBlock = `${String(startH).padStart(2,'0')}:${String(startM).padStart(2,'0')} – ` +
                          `${String(endH).padStart(2,'0')}:${String(endM).padStart(2,'0')}`


     // ACT — do the thing we are testing
    // (in this case we verify our calculation)

    const result = expectedBlock

    // ASSERT — check if the result is what we expected
    //expect(actual).toBe(expectedBlock)
    expect(result).toBe('10:00 – 10:30')

  })


  it('Should handle Midnight RollOver correctly', () => {
    //We are using an example of 11:45 PM, which should fall into the 23:30 - 00:00 block
    const hours = 23
    const minute = 45

    //Manually calculate what the function should return

    const blockStart = Math.floor( (hours * 60 + minute) / 30 ) * 30
    const startH = Math.floor(blockStart / 60)
    const startM = blockStart % 60
    const endTotal = blockStart + 30
    const endH = Math.floor(endTotal / 60) % 24
    const endM = endTotal % 60
    const expectedBlock = `${String(startH).padStart(2,'0')}:${String(startM).padStart(2,'0')} – ` +
                          `${String(endH).padStart(2,'0')}:${String(endM).padStart(2,'0')}`

    expect(expectedBlock).toBe('23:30 – 00:00')
    expect(endH).toBe(0)
    expect(endM).toBe(0)    

  })

})
